from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class WindowData(BaseModel):
    numbers: List[int]
    k: int
class TwoSum(BaseModel):
    values:List[int]
    target:int
class Palindromechecker(BaseModel):
    s:str

@app.post("/max-sum")
def get_max_sum(data: WindowData):
    try:
        nums = data.numbers
        k = data.k
        
        if not nums:
            raise HTTPException(status_code=400, detail="Numbers array cannot be empty")
        if k <= 0:
            raise HTTPException(status_code=400, detail="k must be positive")
        if k > len(nums):
            raise HTTPException(status_code=400, detail="k cannot be larger than array length")
        
        current_sum = sum(nums[:k])
        max_sum = current_sum
        
        for i in range(len(nums) - k):
            current_sum = current_sum - nums[i] + nums[i+k]
            max_sum = max(max_sum, current_sum)
            
        return {"max_sum": max_sum}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
@app.post("/Two-sum")
def findTwosum(data:TwoSum):
    try:
        elements=data.values
        target=data.target
        if  len(elements)==0:
            raise HTTPException(status_code=400,detail="Elements array cannot be empty")
        if len(elements) < 2:
            raise HTTPException(status_code=400, detail="Elements array should contain at least 2 elements")
        preview={}
        for i,num in enumerate(elements):
            diff=target-num
            if diff in preview:
               return {"indices": [preview[diff], i]}  # Fixed: proper JSON format
            preview[num]=i
        return {"indices": []} 
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal server error:{str(e)}")
@app.post("/palindromechecker")
def checkpalindrome(data:Palindromechecker):
    try:
        word=data.s.strip().lower()
        if not word:
            raise HTTPException(status_code=400,detail="word dtring cannot be empty")
        l=0
        r=len(word)-1
        while l<r:
            while l<r and not word[l].isalnum():
                l+=1
            while l<r and not word[r].isalnum():
                r-=1
            if word[l] != word[r]:
                return {"is_palindrome":False}
        return {"is_palindrome":True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error:{str(e)}")

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}