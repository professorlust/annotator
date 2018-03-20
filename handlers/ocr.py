# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2018-03-13 Tuesday
# @email: i@yanshengjia.com
# Copyright 2018 Shengjia Yan. All Rights Reserved.

from .base import *
from time import time

class OCRHandler(BaseHandler):
    def get(self):
        self.get_progress()
        self.get_ocr()

        self.render(
            'ocr.html',
            title='OCR Result Annotation',
            ocr_id=self.application.current_ocr_id,
            image_url=self.application.current_image_url,
            ocr_essay=self.application.current_ocr_essay,
            ocr_correction=self.application.current_ocr_essay,
            corrected_ocr_quantity=self.application.corrected_ocr_quantity,
            sum=self.application.ocr_quantity,
            corrected_ocr_ratio=self.application.corrected_ocr_ratio,
        )
    
    def get_progress(self):
        progress = self.application.db.ocr_progress
        progress_record = progress.find_one()
        self.application.corrected_ocr_quantity = progress_record['corrected_ocr_quantity']
        self.application.corrected_ocr_ratio = float(100 * self.application.corrected_ocr_quantity / self.application.ocr_quantity)

    def get_ocr(self):
        candidates = self.application.db.ocr_candidates
        ocr_record = candidates.find_one()
        self.application.current_ocr_id = ocr_record['ocr_id']
        self.application.current_image_url = self.application.image_url_prefix + ocr_record['image_id']
        self.application.current_ocr_essay = ocr_record['essay']


class OCRSubmitHandler(BaseHandler):
    def post(self):
        ocr_id = int(self.get_argument('ocr_id'))
        image_url = self.get_argument('image_url')
        ocr_correction = self.get_argument('ocr_correction')

        ocr_record = {}
        ocr_record['ocr_id'] = ocr_id
        ocr_record['image_url'] = image_url
        ocr_record['ocr_correction'] = ocr_correction
        ocr_record['time'] = time()

        self.write_db(ocr_record)
        self.get_ocr()
        self.get_progress()

        response = {}
        response['ocr_id'] = self.application.current_ocr_id
        response['image_url'] = self.application.current_image_url
        response['ocr_essay'] = self.application.current_ocr_essay
        response['corrected_ocr_quantity'] = self.application.corrected_ocr_quantity
        response['corrected_ocr_ratio'] = self.application.corrected_ocr_ratio

        self.write(response)

    def get_progress(self):
        progress = self.application.db.ocr_progress
        progress_record = progress.find_one()
        self.application.corrected_ocr_quantity = progress_record['corrected_ocr_quantity']
        self.application.corrected_ocr_ratio = float(100 * self.application.corrected_ocr_quantity / self.application.ocr_quantity)

    def get_ocr(self):
        candidates = self.application.db.ocr_candidates
        ocr_record = candidates.find_one()
        self.application.current_ocr_id = ocr_record["ocr_id"]
        self.application.current_image_url = self.application.image_url_prefix + ocr_record['image_id']
        self.application.current_ocr_essay = ocr_record['essay']

    def write_db(self, record):
        data = self.application.db.ocr_data
        candidates = self.application.db.ocr_candidates
        progress = self.application.db.ocr_progress
        marked = self.application.db.ocr_marked
        ocr_id = record['ocr_id']

        if data.find_one({'ocr_id': ocr_id}) == None:
            data.insert_one(record)

            # corrected_ocr_quantity + 1
            progress.update_one(
                {},
                {'$inc': 
                    {
                        'corrected_ocr_quantity': 1
                    }
                },
            )

            # update annotation list
            progress_record = progress.find_one()
            annotation_list = progress_record['annotation_list']
            annotation_list.append(ocr_id)
            progress.update_one(
                {},
                {'$set': 
                    {
                        'annotation_list': annotation_list
                    }
                }
            )

            # move ocr_record from ocr_candidates to ocr_marked
            ocr_record = candidates.find_one({'ocr_id': ocr_id})
            candidates.delete_one({'ocr_id': ocr_id})
            marked.insert_one(ocr_record)
        else:
            data.update_one(
                {'ocr_id': ocr_id},
                {'$set': record},
                upsert=False
            )

    def close_db(self):
        self.application.conn.close()


class OCRPreviousHandler(BaseHandler):
    def post(self):
        ocr_id = int(self.get_argument('ocr_id'))
        self.get_ocr(ocr_id - 1)

        response = {}
        response['image_url'] = self.application.current_image_url
        response['ocr_essay'] = self.application.current_ocr_essay
        self.write(response)

    def get_ocr(self, ocr_id):
        ocr_record = self.application.ocrs[ocr_id]
        self.application.current_ocr_id = ocr_id
        self.application.current_image_url = self.application.image_url_prefix + ocr_record['image_id']
        self.application.current_ocr_essay = ocr_record['essay']


class OCRNextHandler(BaseHandler):
    def post(self):
        ocr_id = int(self.get_argument('ocr_id'))
        self.get_ocr(ocr_id + 1)

        response = {}
        response['image_url'] = self.application.current_image_url
        response['ocr_essay'] = self.application.current_ocr_essay
        self.write(response)

    def get_ocr(self, ocr_id):
        ocr_record = self.application.ocrs[ocr_id]
        self.application.current_ocr_id = ocr_id
        self.application.current_image_url = self.application.image_url_prefix + ocr_record['image_id']
        self.application.current_ocr_essay = ocr_record['essay']
    