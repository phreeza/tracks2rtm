import milky
from xml.dom import minidom
from time import sleep

class RtmHandler:
    def __init__(self,config):
        self.rtm = milky.API(config.RTM_API_KEY, config.RTM_SHARED_SECRET,
                milky.PERMS_DELETE, token=config.USER_MAIN['token'])
        self.lists = self.rtm.lists.getList()

    def get_list_id_by_name(self, name):
        for _list in self.lists:
            if _list.name == name:
                return _list.id
        return None

    def add_task(self,name,tags='',complete=False,list_id=None):
        if list_id is None:
            list_id = self.get_list_id_by_name(u'Inbox')
        self.tasks = self.rtm.tasks.getList()
        self.list_tasks = self.rtm.tasks.getList(list_id=list_id)
        timeline = self.rtm.timelines.create()
        task = self.rtm.tasks.add(list_id=list_id, name=name, timeline=timeline)
        if tags != u'':
            self.rtm.tasks.addTags(list_id=list_id,task_id=task.taskseries[0].task[0].id,
                taskseries_id=int(task.taskseries[0].id),timeline=timeline,
                tags=tags)
        if complete:
            self.rtm.tasks.complete(list_id=list_id,task_id=task.taskseries[0].task[0].id,
                taskseries_id=int(task.taskseries[0].id),timeline=timeline)
        return task
    def load_tracks_data(self,fname):
        bla = minidom.parse(fname)
        todos = bla.getElementsByTagName('todo')
        projects = bla.getElementsByTagName('project')
        project_dict = dict([(int(pj.getElementsByTagName('id')[0].firstChild.wholeText),{'name':pj.getElementsByTagName('name')[0].firstChild.wholeText}) for pj in projects])
        project_dict
        tags = bla.getElementsByTagName('tag')
        tag_dict = dict([(int(tg.getElementsByTagName('id')[0].firstChild.wholeText),{'name':tg.getElementsByTagName('name')[0].firstChild.wholeText}) for tg in tags])
        todos_dict = dict([(int(td.getElementsByTagName('id')[0].firstChild.wholeText),{'desc':td.getElementsByTagName('description')[0].firstChild.wholeText,'done':not td.getElementsByTagName('completed-at')[0].hasAttribute('nil'),'tags':[]}) for td in todos])
        taggings = bla.getElementsByTagName('tagging')
        for tagging in taggings:
            try:
                todos_dict[int(tagging.getElementsByTagName('taggable-id')[0].firstChild.wholeText)]['tags'].append(tag_dict[int(tagging.getElementsByTagName('tag-id')[0].firstChild.wholeText)]['name'])
            except:
                pass
        for todo in todos:
            try:
                todos_dict[int(todo.getElementsByTagName('id')[0].firstChild.wholeText)]['tags'].append(project_dict[int(todo.getElementsByTagName('project-id')[0].firstChild.wholeText)]['name'])
            except:
                pass

        self.todos_dict = todos_dict

    def add_all(self):
        for (id,todo) in self.todos_dict.iteritems():
            print todo
            self.add_task(todo['desc'],tags=','.join(todo['tags']),complete=todo['done'])
            sleep(1)

if __name__ == '__main__':
    import rtm_configs
    import sys
    handler = RtmHandler(rtm_configs)
    handler.load_tracks_data(sys.argv[-1])
    handler.add_all()
