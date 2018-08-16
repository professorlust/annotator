# Annotator
A Crowdsourcing NLP Annotation Platform with Purview Control and Multiple Quality Control Mechanisms powered by Tornado and MongoDB

## Website

http://mark.17zuoye.net/

## Environment

- python 3.6.2
- tornado 5.0.1
- pymongo 3.6.1
- MongoDB 3.6

## Usage

```shell
> cd /path/to/annotator
> python3 annotator.py
```

## Tasks

* Essay Grading Annotation
* OCR Result Annotation
* Grammar Error Annotation

## Candidate Data Format

* Essay Grading Annotation
  * path: /data/essay/essay.txt
  * format: one line one essay
  * essay_id == line_num - 1
* OCR Result Annotation
  * path: /data/ocr/batch_x/ocr.txt
  * format: one line one scanimage id
  * ocr_id == line_num - 1

## Preview

![demo0](https://raw.githubusercontent.com/yanshengjia/photo/master/annotator_demo_0.png)
![demo4](https://raw.githubusercontent.com/yanshengjia/photo/master/annotator_demo_4.png)
![demo1](https://raw.githubusercontent.com/yanshengjia/photo/master/annotator_demo_1.png)
![demo3](https://raw.githubusercontent.com/yanshengjia/photo/master/annotator_demo_3.png)
![demo6](https://raw.githubusercontent.com/yanshengjia/photo/master/annotator_demo_6.png)