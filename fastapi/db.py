from motor import motor_asyncio
import datetime
import os


MONGO_USERNAME = os.getenv('MONGO_USERNAME', "octa")
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD' , "octa")
MONGO_HOST = os.getenv('MONGO_HOST', "localhost")
MONGO_DATABASE = os.getenv('MONGO_DATABASE', "OCTA")


class Database:
    __client = motor_asyncio.AsyncIOMotorClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:27018/{MONGO_DATABASE}')
    __db = __client[MONGO_DATABASE]

    @staticmethod
    async def get_collection(collection):
        return Database.db[collection]
    
    @staticmethod
    async def student_status(data):
        print(data)
        class_id = data['classId']
        class_collection = f"class{class_id}"
        time = datetime.datetime.now()
        time = time.timestamp()
        student_id = data['studentId']
        resp = await Database.__db[class_collection].update_one(
            {'_id': class_id},
            {'$push': {
                f"session.{student_id}": {
                    'faceState': data["faceState"], 
                    "tabStatus": data["tabStatus"], 
                    "faces": data['faces'], 
                    "studentId": data['studentId'], 
                    "timeStamp": time, 
                    "classId": data['classId']
                    }
                }
            }, False, False
        )
        print(resp.raw_result)
        element =  Database.__db[class_collection].find({"_id": class_id})
        if element is None:
            print(element)
            return {"message": "Class not found"}

        else:
            try:
                if f"{data['studentId']}" not in element['session']:
                    resp = Database.__db[class_collection].update_one({"classId": class_id}, {"$set": {f"session.{data['studentId']}": []}})
            except Exception:
                pass
        return resp.raw_result
