from flask import Flask , render_template, request
import pytube

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    url = request.args.get("url")
    if (url == None):
        return render_template("index.html")

    youtube = pytube.YouTube(url)

    # git video lists 
    vedio_only = youtube.streams.filter(progressive=False,type="video").order_by('resolution')
    vedio = youtube.streams.filter(progressive=True)
    audio = youtube.streams.filter(type="audio")

    # declare video info 
    img = youtube.thumbnail_url
    title = youtube.title
    info = {"img":img,"title":title}

    # init list of type 
    list_vedio_only = []
    list_vedio = []
    list_audio = []

    # make object of vedio only 
    temp = "0"
    for i in vedio_only:  
        if i.resolution != temp:
            temp = i.resolution
            list_vedio_only.append({"type":"vedio only","res":i.resolution,"url":i.url})

    # make list of vedio&audio 
    for i in vedio:
        list_vedio.append({"type":"vedio&audio","res":i.resolution,"url":i.url})

    # make list of audio only 
    for i in audio:
        list_audio.append({"type":i.type,"res":i.abr,"url":i.url})


    # render templates 
    return render_template("index.html" ,data={
        "info":info,
        "vedio_only":list_vedio_only,
        "vedio":list_vedio,
        "audio":list_audio
        })


app.run()
