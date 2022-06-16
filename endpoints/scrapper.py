from typing import List
import requests
from fastapi import Request, Form, HTTPException, APIRouter
from bson.objectid import ObjectId
from fastapi.templating import Jinja2Templates




from services.scrapper import Scraper
from settings import get_db


router = APIRouter()
db = get_db()
templates = Jinja2Templates(directory="static")


############ DEMO #########
@router.get("/")
async def page_name(request: Request):
    result = "Type a page name and submit"
    return templates.TemplateResponse("index.html", context = {"request": request, "result": result, "page_name":""})

@router.post("/")
async def page_name(request: Request, page_name: str = Form(...)):
    try:
        s = Scraper(page_name)
        scraped_data = s.scraping()
        posts = await s.save_records(scraped_data)
        return templates.TemplateResponse("index.html", context = {"request": request, "result": posts})
    except:
        return templates.TemplateResponse("index.html", context = {"request": request, "result": {"error" : "page not found or a problem was accured"}})  
############################




@router.post("/scrape")
async def scraping(request: Request):
    request = await request.json()
    try:
        s = Scraper(request["page_name"])
        scraped_data = s.scraping()
        posts = await s.save_records(scraped_data)
        return {"data":posts}
    except Exception as e:
        return {"error" : str(e)}

@router.get("/all_posts")
async def all_page_posts(request: Request):
    request = await request.json()
    posts = await Scraper(request["page_name"]).get_all()
    return {"page_name": request["page_name"] , "data": posts}


@router.get("/all_scrapped_pages")
async def scrapped_pages():
    pages = await db.list_collection_names()
    return {"pages" : pages}

