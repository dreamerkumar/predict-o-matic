#!/usr/bin/env python3
"""
FastAPI server that wraps calculator.py CLI script.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import subprocess
import sys
from typing import Literal


app = FastAPI(
    title="Calculator API",
    description="A simple calculator API that wraps a CLI script",
    version="1.0.0"
)


class CalculationRequest(BaseModel):
    """Request model for calculation endpoint."""
    operation: Literal["add", "multiply"] = Field(
        ...,
        description="The operation to perform: add or multiply"
    )
    param1: float = Field(..., description="First number")
    param2: float = Field(..., description="Second number")


class CalculationResponse(BaseModel):
    """Response model for calculation endpoint."""
    result: float
    operation: str
    param1: float
    param2: float


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    details: str = ""


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "/calculate": "POST - Perform addition or multiplication",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    """
    Perform a calculation using the CLI calculator script.
    
    Args:
        request: CalculationRequest with operation, param1, and param2
        
    Returns:
        CalculationResponse with the result
        
    Raises:
        HTTPException: If the calculation fails
    """
    try:
        # Call the calculator.py script
        result = subprocess.run(
            [
                sys.executable,
                'calculator.py',
                request.operation,
                str(request.param1),
                str(request.param2)
            ],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        
        # Check if the process succeeded
        if result.returncode != 0:
            error_message = result.stderr.strip() if result.stderr else "Unknown error"
            raise HTTPException(
                status_code=400,
                detail=f"Calculator error: {error_message}"
            )
        
        # Parse the result
        try:
            calculation_result = float(result.stdout.strip())
        except ValueError:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid output from calculator: {result.stdout}"
            )
        
        return CalculationResponse(
            result=calculation_result,
            operation=request.operation,
            param1=request.param1,
            param2=request.param2
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Calculator process timed out"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

