from flask import Flask, request, session, redirect, url_for
from flask import render_template_string, send_from_directory
import os
import base64
import uuid

app = Flask(__name__)

# =========================
# SOZLAMALAR
# =========================

app.secret_key = "pictures_secret_key_2026"

ADMIN_PASSWORD = "Nur1k.st"

PHOTO_FOLDER = "pictures"

os.makedirs(PHOTO_FOLDER, exist_ok=True)


# =========================
# ASOSIY SAHIFA
# =========================

HOME = """
<!DOCTYPE html>
<html lang="kaa">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Pictures</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #f5f5f5;
    color: #222;
    font-family: Arial, sans-serif;
}

header {
    background: white;
    height: 65px;
    padding: 0 18px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    border-bottom: 1px solid #ddd;
}

.logo {
    font-size: 25px;
    font-weight: bold;
}

.admin {
    text-decoration: none;
    color: #222;

    border: 1px solid #ccc;
    padding: 9px 13px;

    border-radius: 8px;
}

.container {
    max-width: 600px;
    margin: auto;
    padding: 25px 18px;
}

.card {
    background: white;
    padding: 22px;

    border-radius: 15px;

    box-shadow: 0 2px 10px #ddd;
}

.info {
    background: #f1f1f1;
    padding: 15px;

    border-radius: 10px;

    line-height: 1.5;
}

button {
    width: 100%;

    padding: 14px;
    margin-top: 15px;

    border: 0;
    border-radius: 10px;

    background: #222;
    color: white;

    font-size: 16px;
}

button:active {
    transform: scale(0.98);
}

video {
    width: 100%;

    margin-top: 15px;

    border-radius: 12px;

    background: black;

    display: none;
}

#takeButton {
    display: none;
}

#switchButton {
    display: none;
}

#message {
    text-align: center;
    margin-top: 15px;
}

</style>

</head>


<body>


<header>

<div class="logo">
Pictures
</div>

<a class="admin" href="/admin">
Admin paneli
</a>

</header>


<div class="container">

<div class="card">


<h2>📷 Súwretke túsiw</h2>


<div class="info">

Kameraǵa ruxsat bergeninen keyin,
súwretke túsiw túymesin basıń.

Súwret alınǵannan keyin administrator
panelinde kórinedi.

</div>


<button onclick="openCamera()">
📷 Kameranı ashıw
</button>


<video
id="video"
autoplay
playsinline>
</video>


<button
id="switchButton"
onclick="switchCamera()">

🔄 Aldı / Artqı kamera

</button>


<button
id="takeButton"
onclick="takePhoto()">

📸 Súwretke túsiw

</button>


<canvas
id="canvas"
style="display:none;">
</canvas>


<div id="message"></div>


</div>

</div>


<script>

let stream = null;

let camera = "user";


/* =========================
   KAMERA ASHIW
========================= */

async function openCamera() {

    try {

        if (stream) {

            stream.getTracks().forEach(
                function(track) {
                    track.stop();
                }
            );

        }


        stream =
            await navigator.mediaDevices.getUserMedia({

                video: {
                    facingMode: camera,

                    width: {
                        ideal: 1920
                    },

                    height: {
                        ideal: 1080
                    }
                },

                audio: false

            });


        const video =
            document.getElementById("video");


        video.srcObject = stream;

        video.style.display = "block";


        document.getElementById(
            "takeButton"
        ).style.display = "block";


        document.getElementById(
            "switchButton"
        ).style.display = "block";


        document.getElementById(
            "message"
        ).innerText =
            "✅ Kamera ashıldı.";


    } catch (error) {

        console.log(error);


        document.getElementById(
            "message"
        ).innerText =
            "❌ Kameraǵa ruxsat berilmedi.";

    }

}


/* =========================
   ALDI / ARTQI KAMERA
========================= */

async function switchCamera() {

    if (camera === "user") {

        camera = "environment";

    } else {

        camera = "user";

    }

    await openCamera();

}


/* =========================
   SÚWRET ALIW
========================= */

async function takePhoto() {

    const video =
        document.getElementById("video");


    const canvas =
        document.getElementById("canvas");


    if (video.videoWidth === 0) {

        alert(
            "Kamera ele tayar emes."
        );

        return;

    }


    canvas.width =
        video.videoWidth;


    canvas.height =
        video.videoHeight;


    const ctx =
        canvas.getContext("2d");


    ctx.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );


    const image =
        canvas.toDataURL(
            "image/jpeg",
            0.95
        );


    document.getElementById(
        "message"
    ).innerText =
        "⏳ Súwret saqlanbaqta...";


    try {

        const response =
            await fetch(
                "/upload",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                        "application/json"
                    },

                    body: JSON.stringify({
                        image: image
                    })

                }
            );


        const data =
            await response.json();


        document.getElementById(
            "message"
        ).innerText =
            data.message;


        if (stream) {

            stream.getTracks().forEach(
                function(track) {
                    track.stop();
                }
            );

        }


        video.style.display = "none";


        document.getElementById(
            "takeButton"
        ).style.display = "none";


        document.getElementById(
            "switchButton"
        ).style.display = "none";


    } catch (error) {

        console.log(error);


        document.getElementById(
            "message"
        ).innerText =
            "❌ Súwret saqlawda qáte boldı.";

    }

}

</script>


</body>

</html>
"""


# =========================
# LOGIN
# =========================

LOGIN = """
<!DOCTYPE html>
<html lang="kaa">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Pictures Admin</title>

<style>

body {
    margin: 0;
    background: #f5f5f5;
    font-family: Arial;
}

.box {
    max-width: 400px;

    margin: 100px auto;

    background: white;

    padding: 25px;

    border-radius: 15px;

    box-shadow: 0 2px 10px #ddd;
}

input {
    width: 100%;

    padding: 13px;

    margin-top: 10px;

    border: 1px solid #ccc;

    border-radius: 8px;

    font-size: 16px;
}

button {
    width: 100%;

    padding: 13px;

    margin-top: 15px;

    border: 0;

    border-radius: 8px;

    background: #222;

    color: white;

    font-size: 16px;
}

.error {
    color: red;
}

</style>

</head>


<body>


<div class="box">


<h2>🔐 Pictures Admin</h2>


<form method="POST">


<input
type="password"
name="password"
placeholder="Admin paroli"
required
>


<button type="submit">
Kiriw
</button>


</form>


{% if error %}

<p class="error">
{{ error }}
</p>

{% endif %}


</div>


</body>

</html>
"""


# =========================
# ADMIN PANEL
# =========================

ADMIN = """
<!DOCTYPE html>
<html lang="kaa">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Pictures Admin</title>

<style>

body {
    margin: 0;

    background: #f5f5f5;

    font-family: Arial;
}

header {
    background: white;

    padding: 18px;

    border-bottom: 1px solid #ddd;

    display: flex;

    justify-content: space-between;
}

.container {
    max-width: 800px;

    margin: auto;

    padding: 20px;
}

.photo {
    background: white;

    padding: 12px;

    margin-bottom: 20px;

    border-radius: 15px;

    box-shadow: 0 2px 10px #ddd;
}

.photo img {
    display: block;

    width: 100%;

    height: auto;

    border-radius: 10px;
}

.delete {
    display: block;

    margin-top: 12px;

    background: #d11;

    color: white;

    text-decoration: none;

    text-align: center;

    padding: 11px;

    border-radius: 8px;
}

.logout {
    color: #222;

    text-decoration: none;
}

</style>

</head>


<body>


<header>

<strong>
Pictures — Admin
</strong>


<a
class="logout"
href="/logout">

Shıǵıw

</a>

</header>


<div class="container">


<h2>
📸 Alınǵan súwretler
</h2>


{% if photos %}


{% for photo in photos %}


<div class="photo">


<img
src="{{ url_for('show_photo', filename=photo) }}"
alt="Picture"
>


<p>
📷 {{ photo }}
</p>


<a
class="delete"
href="{{ url_for('delete_photo', filename=photo) }}"
>

🗑️ Óshiriw

</a>


</div>


{% endfor %}


{% else %}


<p>
Házirge súwret alınbaǵan.
</p>


{% endif %}


</div>


</body>

</html>
"""


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template_string(
        HOME
    )


# =========================
# UPLOAD
# =========================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    data = request.get_json()

    if not data:

        return {
            "message":
            "❌ Maǵlıwmat kelmedi."
        }


    image = data.get("image")

    if not image:

        return {
            "message":
            "❌ Súwret tabılmadı."
        }


    try:

        image_data = image.split(
            ",",
            1
        )[1]

        image_bytes = base64.b64decode(
            image_data
        )

    except Exception:

        return {
            "message":
            "❌ Súwret formatı qáte."
        }


    filename = (
        uuid.uuid4().hex
        + ".jpg"
    )


    filepath = os.path.join(
        PHOTO_FOLDER,
        filename
    )


    with open(
        filepath,
        "wb"
    ) as file:

        file.write(
            image_bytes
        )


    return {
        "message":
        "✅ Súwret tabıslı saqlandı!"
    }


# =========================
# ADMIN LOGIN
# =========================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    if session.get("admin"):

        photos = []


        for filename in os.listdir(
            PHOTO_FOLDER
        ):

            if filename.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                photos.append(
                    filename
                )


        photos.sort(
            reverse=True
        )


        return render_template_string(
            ADMIN,
            photos=photos
        )


    error = ""


    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )


        if password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect(
                url_for("admin")
            )


        error = "❌ Parol qáte!"


    return render_template_string(
        LOGIN,
        error=error
    )


# =========================
# SÚWRET KÓRSETIW
# =========================

@app.route(
    "/photo/<filename>"
)
def show_photo(filename):

    if not session.get("admin"):

        return (
            "❌ Ruxsat joq!",
            403
        )


    filename = os.path.basename(
        filename
    )


    return send_from_directory(
        PHOTO_FOLDER,
        filename
    )


# =========================
# SÚWRET ÓSHIRIW
# =========================

@app.route(
    "/delete/<filename>"
)
def delete_photo(filename):

    if not session.get("admin"):

        return (
            "❌ Ruxsat joq!",
            403
        )


    filename = os.path.basename(
        filename
    )


    filepath = os.path.join(
        PHOTO_FOLDER,
        filename
    )


    if os.path.exists(filepath):

        os.remove(filepath)


    return redirect(
        url_for("admin")
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================
# SERVER
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )


    print("")
    print("==============================")
    print("       PICTURES ISKE TUSTI")
    print("==============================")
    print("")
    print("Osi telefonda:")
    print(
        "http://127.0.0.1:"
        + str(port)
    )
    print("")
    print("Server port:")
    print(port)
    print("")
    print("==============================")


    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )