import uvicorn


def main():
    print("Starting FastAPI backend...")
    uvicorn.run("taxipred.backend.api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
