from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.post("/test", response_class=HTMLResponse)
async def test_post(select_scraper: str = Form(...), input_id: str = Form(...)):
    # Process the data
    print(f"Scraper: {select_scraper}, ID: {input_id}")
    
    content: str = f"""
        <div class="alert alert-success">
            <p>Scraper <strong>{select_scraper}</strong> started for ID <strong>{input_id}</strong>!</p>
        </div>
    """
    headers = {
        "HX-Trigger": json.dumps({"itemAdded": {"scraper": select_scraper + " " + "header!!"}})
    }
    return HTMLResponse(content=content, headers=headers)


@app.post("/test2")
async def test_redirect(select_scraper: str = Form(...), input_id: str = Form(...)):
    # Logic here...
     print(f"Scraper: {select_scraper}, ID: {input_id}")
     return Response(headers={"HX-Redirect": "/dashboard"})

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        name="index.page.html",
        context={"request": request, "page_title": "Home"},
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        name="dashboard.page.html",
        context={"request": request}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)