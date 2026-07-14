from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/info')
def get_video_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "url parameter is required"}), 400
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['webpage']
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            best_audio_url = None
            for f in info.get('formats', []):
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    best_audio_url = f.get('url')
                    break
            
            formats_dict = {}
            for f in info.get('formats', []):
                if not f.get('url') or f.get('vcodec') == 'none' or f.get('vcodec') is None:
                    continue
                
                height = f.get('height')
                if not height:
                    continue
                    
                quality_label = f"{height}p"
                has_audio = f.get('acodec') != 'none' and f.get('acodec') is not None
                
                if quality_label not in formats_dict or (has_audio and not formats_dict[quality_label]['is_merged']):
                    formats_dict[quality_label] = {
                        "quality": quality_label,
                        "video_url": f.get('url'),
                        "audio_url": f.get('url') if has_audio else best_audio_url,
                        "is_merged": has_audio,
                        "ext": f.get('ext', 'mp4')
                    }
            
            formats = list(formats_dict.values())
            formats.sort(key=lambda x: int(x['quality'].replace('p', '')), reverse=True)
            
            return jsonify({
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "formats": formats
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ক্লাউডফ্লেয়ার ওয়ার্কার্সের জন্য হ্যান্ডলার
def Workers(request):
    return app(request)
