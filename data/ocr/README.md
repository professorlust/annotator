# About Data

* essay_data.json: 从公司数据库中挖出来的6万多篇英语作文的扫描图片数据，包含总分、题干、题号
  * image_id
  * total_score
  * prompt
  * problem_id
  * paper_id
* ocr.txt: essay_data.json 中 prompt 非空的图片数据
  * image_id
  * essay: a2ia 识别出的作文文本
* ocr_data.txt: 扫描作文图片标注数据，包含人工标注的作文文本
  * _id
  * time
  * ocr_correction: 人工标注作文文本
  * image_url
  * ocr_id: ocr.txt 中的字典编号，第一个字典的 ocr_id 为0
  * annotator