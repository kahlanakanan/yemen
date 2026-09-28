from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/get-video-info")
def get_video_info(url: str):
    ydl_opts = {
        'extract_flat': False,
        'skip_download': True, # أهم نقطة: امنع بايثون من تحميل الفيديو نهائياً
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            formats_list = []
            for f in info.get('formats', []):
                # تصفية الصيغات المفيدة (فيديو مع صوت أو صوت فقط)
                if f.get('url') and (f.get('ext') == 'mp4' or f.get('acodec') != 'none'):
                    formats_list.append({
                        "format_id": f.get('format_id'),
                        "resolution": f.get('resolution') or f.get('format_note', 'Audio Only'),
                        "ext": f.get('ext'),
                        "url": f.get('url') # هذا هو الرابط المباشر من المصدر
                    })
                    
            return {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "formats": formats_list
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
