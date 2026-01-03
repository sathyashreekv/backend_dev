from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import logging
from datetime import datetime
import time
from sqlalchemy.orm import Session
from database import get_db, APIRequest

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware to log requests
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Log to database (we'll add this functionality)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    db=next(get_db())
    db_request = APIRequest(
        endpoint=request.url.path,
        method=request.method,
        response_time=process_time,
        status_code=response.status_code
    )
    db.add(db_request)
    db.commit()
    db.close()
    
    return response

class WindowData(BaseModel):
    numbers: List[int]
    k: int
class TwoSum(BaseModel):
    values:List[int]
    target:int
class PalindromeChecker(BaseModel):
    s: str

@app.post("/max-sum")
def get_max_sum(data: WindowData):
    logger.info(f"Max-sum request: array_length={len(data.numbers)}, k={data.k}")
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
def checkpalindrome(data: PalindromeChecker):
    try:
        word = data.s.strip().lower()
        if not word:
            raise HTTPException(status_code=400, detail="String cannot be empty")
        
        l = 0
        r = len(word) - 1
        
        while l < r:
            # Skip non-alphanumeric characters from left
            while l < r and not word[l].isalnum():
                l += 1
            # Skip non-alphanumeric characters from right
            while l < r and not word[r].isalnum():
                r -= 1
            
            if word[l] != word[r]:
                return {"is_palindrome": False}
            
            l += 1  # Missing: move left pointer
            r -= 1  # Missing: move right pointer
        
        return {"is_palindrome": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}
