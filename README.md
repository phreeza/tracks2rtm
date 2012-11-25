tracks2rtm
==========

Tool to import data from [Tracks GTD](http://getontracks.org/) to [Remember The Milk](http://www.rememberthemilk.com/).

It reads the output of the Tracks XML export function and inserts the tasks into your Remember the Milk account.

Functionality is currently very rudimentary. Only tags and projects are imported (projects are treated as tags). Due dates, notes, contexts, etc. are missing. They should be straightforward to add if you read the code though.

*Warning:* this is a quick hack, and in no way should it be considered safe to transfer critical information. That said, there isn't much it can really do wrong, so just give it a try and make sure you double check the results.

Requirements
---
tracks2rtm uses the [milky](http://bitbucket.org/Surgo/milky/) python bindings for the RTM API.
Usage
---
 1. update the information in rtm_config.py using your API key.
 2. run ```python tracks2rtm.py /path/to/tracks-export.xml```
 3. Watch the magic happen.

