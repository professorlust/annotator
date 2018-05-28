# Data

* essay_items_info.txt 英语作文题目信息 单行 JSON
  * type: 题目类型
  * type_mean: 题目类型含义
  * item_id: 题目 id
  * stem_plain: 题干文本
  * stem_plain_qs: list，题目中的小问
* paper_id_to_grade.txt 考卷 id 与年纪的对应
  * paper_id: grade
* essay_scandata.txt 学生作文的扫描图片数据 单行 JSON
  - paper_id: 回答所属的考卷 id
  - url: list 回答的扫描图片url
  - total_score: 总分
  - score: 得分
  - number: 该小问的题号，从0开始
  - item_id: 题目 id