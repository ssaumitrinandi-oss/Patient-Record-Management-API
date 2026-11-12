from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

app= FastAPI()

class Patient(BaseModel):
    id: Annotated[str,Field(...,description='enter patient ID',examples=['p001'])]
    name:Annotated[str,Field(...,description='enter patient name')]
    city:Annotated[str,Field(...,description='enter city name')]
    age:Annotated[int,Field(...,description='age of the patient',gt=0,lt=120)]
    gender:Annotated[Literal['male','female','others'],Field(...,description='gender of the patient')]
    height:Annotated[float, Field(...,gt=0,description='height of the patient in meters')]
    weight:Annotated[float, Field(...,gt=0,description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'over weight'
        else:
            return 'obese'
        
#creating a new pydantic model for upadations
class PatientUpdate(BaseModel):
        name:Annotated[Optional[str],Field(default=None)]
        city:Annotated[Optional[str],Field(default=None)]
        age:Annotated[Optional[int],Field(default=None,gt=0,lt=120)]
        gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
        height:Annotated[Optional[float],Field(default=None,gt=0)]
        weight:Annotated[Optional[float],Field(default=None,gt=0)]


#existing--> update 
def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f) #dump() = Write Python data into a JSON file.

     

@app.get("/")
def hello():
    return {"message":"patient management system API"}

@app.get("/about")
def about():
    return {"message":"a fully functional API to manage your patient records"}

@app.get("/view")
def view():
     data = load_data()
     return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str= Path(...,description='id of the patient',examples='p001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404,detail='patient not found')

@app.get("/sort")
def sort_patients(sort_by: str=Query(...,description='sort on the basis of height,weight or bmi'),order: str=Query('asc',description="sort indescending or descending order")):
 ##here order id optional ,we didnot use...

    valid_fields=["height","weight","bmi"]
    if sort_by not in valid_fields:
      raise HTTPException(status_code=400,detail=f'invalid field ,select from {valid_fields}')
    if order not in ["asc","desc"]:
        raise HTTPException (status_code=400,detail='invalid selection between asc ,desc')

    data=load_data()

    sort_order= True if order=="desc" else False
    sorted_data=sorted(data.values(), key=lambda x : x.get(sort_by,0),reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient:Patient):

    #load existing 
    data=load_data()

    #check if data exists already
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exist')
     #add new data to data base
     # here we have to covert python object int a dict
     
    data[patient.id] = patient.model_dump(exclude=['id']) #model_dump: converts python objects to a py dictionary

    #save into the json file
    save_data(data)
    return JSONResponse(status_code=201,content={'message':'Patient created successfully'})

@app.put('/edit/{patient_id}')
def upadate_patient(patient_id:str , patient_update:PatientUpdate):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    existing_patient_info=data[patient_id]
    #converting patient_update into dict as we need to put the udated data into existing_patient_info which is a dict 
    updated_patient_info=patient_update.model_dump(exclude_unset=True) #exclude_unset=True:This helps you identify only the fields the user actually supplied.It is used to exclude fields that were not explicitly provided when creating the Pydantic object.

    for key,value in updated_patient_info.items():
        existing_patient_info[key]=value
        #existing_patient_info -> pydantic_obj -> to trigger/update bmi,verdict

    existing_patient_info['id']=patient_id #adding id key into the pydantic obj as it was not in that class

    patient_pydantic_obj=Patient(**existing_patient_info) 

        #->patient_pydantic_obj -> dict
    existing_patient_info=patient_pydantic_obj.model_dump(exclude='id') #excluding id

        #add this dict to data
    data[patient_id]=existing_patient_info

        #save data
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient updated'})

        #delete patient

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
            data=load_data()
            if patient_id not in data:
                raise HTTPException(status_code=404,detail={'message':'patient not found'}) 
            del data[patient_id]
            save_data(data)

            return JSONResponse(status_code=200,content={'message':'patient deleted'})

