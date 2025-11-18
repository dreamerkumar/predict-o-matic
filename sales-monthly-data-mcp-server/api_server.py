#!/usr/bin/env python3
"""
FastAPI server that wraps sales_data.py CLI script.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import subprocess
import sys
from typing import Optional


app = FastAPI(
    title="Sales Data API",
    description="API for retrieving monthly sales data",
    version="1.0.0"
)


class SalesDataResponse(BaseModel):
    """Response model for sales data endpoint."""
    month: str
    year: str
    sales: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    details: str = ""


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Sales Data API",
        "version": "1.0.0",
        "endpoints": {
            "/sales": "GET - Retrieve sales data by month and year",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/sales", response_model=SalesDataResponse)
async def get_sales(
    month: str = Query(..., description="Month (e.g., January, February)"),
    year: str = Query(..., description="Year (e.g., 2023, 2024)")
):
    """
    Retrieve sales data for the specified month and year.
    
    Args:
        month: Month (e.g., January, February)
        year: Year (e.g., 2023, 2024)
        
    Returns:
        SalesDataResponse with the month, year, and sales data
        
    Raises:
        HTTPException: If the sales data is not found or an error occurs
    """
    try:
        # Call the sales_data.py script
        result = subprocess.run(
            [
                sys.executable,
                'sales_data.py',
                month,
                year
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
                detail=f"Sales data error: {error_message}"
            )
        
        # Parse the result
        sales_data = result.stdout.strip()
        
        if sales_data == "No data exists":
            raise HTTPException(
                status_code=404,
                detail=f"No sales data found for {month} {year}"
            )
        
        return SalesDataResponse(
            month=month.strip().capitalize(),
            year=year.strip(),
            sales=sales_data
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Sales data process timed out"
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
