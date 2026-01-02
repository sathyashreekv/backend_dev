from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class WindowData(BaseModel):
    numbers: List[int]
    k: int
class TwoSum(BaseModel):
    values:List[int]
    target:int

@app.post("/max-sum")
def get_max_sum(data: WindowData):
    # Your Sliding Window Logic here
    nums = data.numbers
    k = data.k
    if not nums or k > len(nums):
        return {"error": "Invalid input"}
    
    current_sum = sum(nums[:k])
    max_sum = current_sum
    
    for i in range(len(nums) - k):
        current_sum = current_sum - nums[i] + nums[i+k]
        max_sum = max(max_sum, current_sum)
        
    return {"max_sum": max_sum}
@app.post("/Two-sum")
def findTwosum(data:TwoSum):
    elements=data.values
    target=data.target  # Fixed: was data.k, should be data.target
    preview={}
    for i,num in enumerate(elements):
        diff=target-num
        if diff in preview:
            return {"indices": [preview[diff], i]}  # Fixed: proper JSON format
        preview[num]=i
    return {"indices": []}  # Fixed: proper JSON format

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}