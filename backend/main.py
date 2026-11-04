
import json
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# --------------------------------------------------
# APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="ReproTrace AI API",
    description="Evidence-based debugging investigation engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# BUG REPORT MODEL
# --------------------------------------------------

class BugReport(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=5000)
    error_log: str = Field(default="", max_length=10000)
    language: str = Field(default="Python", max_length=50)


# --------------------------------------------------
# LOCAL RULE-BASED DEBUGGING ENGINE
# --------------------------------------------------

def demo_analysis(report: BugReport) -> dict[str, Any]:

    title = report.title
    description = report.description
    error_log = report.error_log

    combined = (
        title + " " +
        description + " " +
        error_log
    ).lower()

    evidence = []
    causes = []
    steps = []
    checks = []
    candidate_test = ""

    # RULE 1: DIVISION BY ZERO

    if (
        "zerodivisionerror" in combined
        or "division by zero" in combined
    ):
        summary = (
            "The application may be failing because "
            "a division operation received zero as its denominator."
        )

        evidence = [
            "The submitted report mentions division by zero.",
            "The error is consistent with a ZeroDivisionError."
        ]

        causes = [
            {
                "cause": "Denominator is zero.",
                "likelihood": "High",
                "reasoning": (
                    "The division operation may receive zero "
                    "as its second operand."
                )
            },
            {
                "cause": "Missing input validation.",
                "likelihood": "Medium",
                "reasoning": (
                    "The application may not validate the "
                    "denominator before performing division."
                )
            }
        ]

        steps = [
            "Open the calculator application.",
            "Enter a number as the first operand.",
            "Enter zero as the second operand.",
            "Select the division operation.",
            "Observe the reported error."
        ]

        candidate_test = (
            "Provide zero as the denominator and check "
            "whether the application handles the input safely."
        )

        checks = [
            "Inspect the denominator before division.",
            "Check whether zero-value validation exists.",
            "Compare expected behaviour with actual behaviour."
        ]

    # RULE 2: INVALID LIST INDEX

    elif (
        "indexerror" in combined
        or "list index out of range" in combined
    ):
        summary = (
            "The application may be accessing a list element "
            "outside its valid index range."
        )

        evidence = [
            "The submitted report mentions an index-related error."
        ]

        causes = [
            {
                "cause": "Invalid list index.",
                "likelihood": "High",
                "reasoning": (
                    "The requested index may be outside "
                    "the available list positions."
                )
            },
            {
                "cause": "Incorrect boundary condition.",
                "likelihood": "Medium",
                "reasoning": (
                    "A loop or conditional may be allowing "
                    "an invalid index."
                )
            }
        ]

        steps = [
            "Run the application.",
            "Provide a list with a limited number of elements.",
            "Trigger the operation that accesses the list.",
            "Observe whether an invalid index is requested."
        ]

        candidate_test = (
            "Test list access with an index equal to "
            "the list length and verify safe handling."
        )

        checks = [
            "Inspect the list length.",
            "Check the requested index.",
            "Review loop and boundary conditions."
        ]

    # RULE 3: MISSING DICTIONARY KEY

    elif "keyerror" in combined:
        summary = (
            "The application may be trying to access "
            "a dictionary key that does not exist."
        )

        evidence = [
            "The submitted report contains a KeyError reference."
        ]

        causes = [
            {
                "cause": "Missing dictionary key.",
                "likelihood": "High",
                "reasoning": (
                    "The requested key may not be present "
                    "in the dictionary."
                )
            }
        ]

        steps = [
            "Run the application.",
            "Provide dictionary data without the expected key.",
            "Trigger the dictionary lookup.",
            "Observe the resulting behaviour."
        ]

        candidate_test = (
            "Test dictionary access when the requested key "
            "is missing."
        )

        checks = [
            "Inspect the dictionary contents.",
            "Verify that the requested key exists.",
            "Check whether missing keys are handled."
        ]

    # RULE 4: TYPE ERROR

    elif "typeerror" in combined:
        summary = (
            "The application may be performing an operation "
            "with incompatible data types."
        )

        evidence = [
            "The submitted report mentions a TypeError."
        ]

        causes = [
            {
                "cause": "Incompatible data types.",
                "likelihood": "High",
                "reasoning": (
                    "An operation may be receiving a value "
                    "of an unexpected type."
                )
            },
            {
                "cause": "Missing type conversion.",
                "likelihood": "Medium",
                "reasoning": (
                    "Input values may not be converted "
                    "before the operation."
                )
            }
        ]

        steps = [
            "Run the application.",
            "Provide inputs with different data types.",
            "Trigger the operation mentioned in the report.",
            "Observe the error."
        ]

        candidate_test = (
            "Test the operation with valid and invalid input types."
        )

        checks = [
            "Inspect the types of input variables.",
            "Check type conversions.",
            "Verify the expected input format."
        ]

    # RULE 5: NAME ERROR

    elif "nameerror" in combined:
        summary = (
            "The application may be referencing a variable "
            "that has not been defined in the current scope."
        )

        evidence = [
            "The submitted report mentions a NameError."
        ]

        causes = [
            {
                "cause": "Undefined variable.",
                "likelihood": "High",
                "reasoning": (
                    "The referenced variable may not have "
                    "been declared or assigned."
                )
            },
            {
                "cause": "Variable naming mismatch.",
                "likelihood": "Medium",
                "reasoning": (
                    "The variable name used may differ "
                    "from its declaration."
                )
            }
        ]

        steps = [
            "Run the application.",
            "Trigger the operation using the reported variable.",
            "Observe the NameError.",
            "Inspect the variable declaration and usage."
        ]

        candidate_test = (
            "Test the function with all required variables defined."
        )

        checks = [
            "Inspect variable declarations.",
            "Check spelling and capitalization.",
            "Review variable scope."
        ]

    # RULE 6: ATTRIBUTE ERROR

    elif "attributeerror" in combined:
        summary = (
            "The application may be trying to access "
            "an unavailable attribute or method."
        )

        evidence = [
            "The submitted report mentions an AttributeError."
        ]

        causes = [
            {
                "cause": "Unavailable attribute.",
                "likelihood": "High",
                "reasoning": (
                    "The object may not provide the requested "
                    "attribute or method."
                )
            },
            {
                "cause": "Unexpected object type.",
                "likelihood": "Medium",
                "reasoning": (
                    "The variable may contain a different "
                    "object type than expected."
                )
            }
        ]

        steps = [
            "Run the application.",
            "Trigger the operation involving the object.",
            "Observe the AttributeError.",
            "Inspect the object and requested attribute."
        ]

        candidate_test = (
            "Test the operation with an object that has "
            "the expected attribute."
        )

        checks = [
            "Inspect the object type.",
            "Check whether the attribute exists.",
            "Review object initialization."
        ]

    # RULE 7: SYNTAX ERROR

    elif "syntaxerror" in combined:
        summary = (
            "The application may contain invalid programming "
            "language syntax."
        )

        evidence = [
            "The submitted report mentions a SyntaxError."
        ]

        causes = [
            {
                "cause": "Invalid syntax.",
                "likelihood": "High",
                "reasoning": (
                    "A missing bracket, colon, quotation mark "
                    "or other syntax element may be present."
                )
            }
        ]

        steps = [
            "Open the source file mentioned in the error.",
            "Inspect the reported line.",
            "Review nearby statements for syntax issues.",
            "Check whether the application starts successfully."
        ]

        candidate_test = (
            "Run a syntax or compilation check after reviewing "
            "the reported source location."
        )

        checks = [
            "Inspect the reported line number.",
            "Check brackets and quotation marks.",
            "Review nearby statements."
        ]

    # RULE 8: UNKNOWN ERROR

    else:
        summary = (
            "The submitted software issue requires further "
            "technical investigation."
        )

        evidence = [
            "A bug title was submitted: " + title,
            "A bug description was provided.",
            (
                "An error log was provided."
                if error_log.strip()
                else "No error log was provided."
            )
        ]

        causes = [
            {
                "cause": "Possible input validation issue.",
                "likelihood": "Unknown",
                "reasoning": (
                    "The available information is insufficient "
                    "to confirm this hypothesis."
                )
            },
            {
                "cause": "Possible application logic issue.",
                "likelihood": "Unknown",
                "reasoning": (
                    "The relevant source code and runtime "
                    "behaviour have not been inspected."
                )
            }
        ]

        steps = [
            "Review the submitted bug description.",
            "Identify expected application behaviour.",
            "Record the actual application behaviour.",
            "Repeat the issue using the same input.",
            "Collect the complete error log."
        ]

        candidate_test = (
            "Create a test using the reported input and "
            "compare the actual result with the expected result."
        )

        checks = [
            "Collect additional error logs.",
            "Inspect the relevant source code.",
            "Compare expected and actual outputs."
        ]

    # FINAL INVESTIGATION REPORT

    result = {
        "summary": summary,
        "evidence": evidence,
        "likely_causes": causes,
        "reproduction_steps": steps,
        "candidate_test": candidate_test,
        "confirmation_or_refutation": checks,
        "limitations": [
            "This report was generated using local rule-based logic.",
            "It is not generated by Meta AI or another external LLM.",
            "The submitted source code has not been executed.",
            "No test has been run.",
            "No fix has been verified."
        ]
    }

    return {
        "status": "analysis_complete",
        "model": "ReproTrace Local Debug Engine",
        "mode": "offline-demo",
        "verified": False,
        "analysis": json.dumps(result, indent=2)
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to ReproTrace AI",
        "status": "running",
        "mode": "offline-demo"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "ReproTrace AI API",
        "mode": "offline-demo"
    }


# --------------------------------------------------
# BUG ANALYSIS ENDPOINT
# --------------------------------------------------

@app.post("/api/analyze")
def analyze(report: BugReport):
    return demo_analysis(report)
