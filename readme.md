'/'：初始界面

'/api/tasks'，methods = ['GET']：查询列表"tasks"

'/api/tasks/<int:task_id>'，methods = ['GET']：用索引查询列表中的某个元素

'/api/tasks'，methods = {'POST'}：往列表"tasks"中加入新元素

'/api/tasks/<int:task_id>'，methods = ['PUT']：用索引更新列表中的某个元素，元素的值为上传的数据

'/api/tasks/<int:task_id>'，methods = ['PATCH']：用索引修改列表中的某个元素，元素的值为修改的数据及未修改的原数据

'/api/tasks/<int:task_id>'，methods=['DELETE']：用索引删除列表中的某个元素