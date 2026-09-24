from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Regalo</title>

<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {

    background: #F7F0EE;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

    font-family: "Press Start 2P", monospace;
}


/* ==============================
   PANTALLA INICIAL
   ============================== */

#inicio {
    width: 100%;
    height: 100%;

    display: flex;
    flex-direction: column;

    justify-content: center;
    align-items: center;

    text-align: center;
}

#pregunta {
    font-family: "Press Start 2P", monospace;
    font-size: 22px;
    line-height: 1.7;

    margin-bottom: 25px;

    color: #222;
}

#nombre {
    width: 320px;

    padding: 15px;

    border: 3px solid #B58697;
    border-radius: 0;

    outline: none;

    font-family: "Press Start 2P", monospace;
    font-size: 12px;

    text-align: center;
}

#nombre::placeholder {
    font-family: "Press Start 2P", monospace;
    font-size: 10px;
}

#boton {
    margin-top: 15px;

    padding: 15px 25px;

    border: 3px solid #B58697;
    border-radius: 0;

    background: #E1A8C4;
    color: #FFF2F7;

    font-family: "Press Start 2P", monospace;
    font-size: 12px;

    cursor: pointer;
}

#boton:active,
#boton.presionado {
    transform: translateY(3px);
    box-shadow: none;
}

#error {
    display: none;

    margin-top: 20px;

    color: red;

    font-family: "Press Start 2P", monospace;
    font-size: 11px;

    line-height: 1.6;

    text-align: center;
}


/* ==============================
   PANTALLA DE BIENVENIDA
   ============================== */

#bienvenida {

    display: none;

    position: absolute;

    inset: 0;

    background: #F7F0EE;

    justify-content: center;

    align-items: center;

    text-align: center;

    z-index: 10;
}

#mensajeBienvenida {

    font-family: "Press Start 2P", monospace;

    font-size: 22px;

    line-height: 1.8;

    color: #222;
}


/* ============================================================
   CANVAS
   ============================================================ */

#canvas {

    display: none;

    position: absolute;

    left: 0;
    top: 0;

    width: 100%;
    height: 100%;

    background: #F7F0EE;

    image-rendering: pixelated;
}

</style>

</head>


<body>


<!-- ==============================
     PANTALLA INICIAL
     ============================== -->

<div id="inicio">

    <div id="pregunta">
        ¿Cuál es tu nombre?
    </div>

    <input
        id="nombre"
        type="text"
        placeholder="Escribe tu nombre..."
    >

    <button id="boton">
        Continuar
    </button>

    <div id="error">
        NO PUEDES RECIBIR ESTE REGALO
    </div>

</div>


<!-- ==============================
     PANTALLA DE BIENVENIDA
     ============================== -->

<div id="bienvenida">

    <div id="mensajeBienvenida"></div>

</div>


<!-- ============================================================
     CANVAS
     ============================================================ -->

<canvas id="canvas"></canvas>


<script>


/* ============================================================
   ⭐ CONFIGURACIÓN
   ============================================================

   AQUÍ PUEDES CAMBIAR LA VELOCIDAD DE APARICIÓN.

   Ahora esta espera SOLO se aplica a los píxeles que
   realmente tienen color (antes se aplicaba también a
   los huecos vacíos, y por eso la animación tardaba
   muchísimo en mostrar algo).

   20  = muy rápido
   50  = rápido
   100 = normal
   250 = lento
   500 = muy lento

   El número está en MILISEGUNDOS.

   Ahora, en vez de un solo número fijo, cada píxel espera
   una cantidad de milisegundos ALEATORIA entre estos dos
   valores, para que la aparición se sienta muy irregular
   y no como una cuenta regresiva pareja.
   ============================================================ */

const TIEMPO_ENTRE_PIXELES_MIN = 7;
const TIEMPO_ENTRE_PIXELES_MAX = 30;


/* ============================================================
   ⭐ NOMBRES PERMITIDOS
   ============================================================

   Solo estos nombres pueden ver el regalo. Cualquier otro
   nombre muestra el mensaje de error. La comparación no
   distingue mayúsculas/minúsculas ni espacios extra.

   ============================================================ */

const NOMBRES_PERMITIDOS = ["sally", "marie"];


/* ============================================================
   ⭐ TAMAÑO DEL DIBUJO
   ============================================================

   Tu dibujo de Coddy es de:

   64 x 64

   NO CAMBIES ESTO.

   ============================================================ */


const ANCHO = 64;
const ALTO = 64;


/* ============================================================
   ⭐⭐⭐ TU DIBUJO DE CODDY ⭐⭐⭐

   PEGA AQUÍ EXACTAMENTE EL CÓDIGO.

   NOTA: tu arreglo original tenía 62 filas en vez de 64,
   y una fila con 65 columnas en vez de 64 (probablemente
   se cortó algo al copiar el dibujo). Lo corregí para que
   quede una cuadrícula 64x64 exacta — pero si vuelves a
   pegar un dibujo nuevo, revisa que también tenga
   exactamente 64 filas de 64 elementos cada una.

   ============================================================ */

const PIXELS = [
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#ffb347", "#ffb347", "#d29641", "#ffb347", null, "#ffb347", "#ffb347", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#d29641", "#ffb347", "#ffecd1", "#d29641", "#d29641", "#ffb347", "#ffb347", "#ffb347", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#758052", null, null, null, "#d29641", "#d29641", "#d29641", null, "#ffb347", "#d29641", null, null, null, null, null, null, "#d29641", "#ffb347", "#f4c076", "#ffecd1", "#d29641", "#d29641", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#758052", "#d29641", "#d29641", "#d29641", "#ffb347", "#ffd79e", "#ffd79e", "#ffb347", "#d29641", null, "#a2a75c", "#a2a75c", null, null, null, "#d29641", "#ffb347", "#f4c076", "#ffb347", "#ffecd1", "#d29641", "#d29641", "#d29641", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#d29641", "#d29641", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#a2a75c", "#a2a75c", null, null, null, "#d29641", "#ffb347", "#f4c076", "#ffb347", "#ffb347", "#ffecd1", "#d29641", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#d29641", "#d29641", "#ffecd1", "#d29641", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#d29641", "#ffb347", null, "#a2a75c", null, "#5e6836", "#5e6836", "#d29641", "#ffb347", "#ffb347", "#f4c076", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#d29641", "#ffb347", "#ffb347", "#ffecd1", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#a2a75c", null, "#5e6836", "#5e6836", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffecd1", "#d29641", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#f4c076", "#d29641", "#a2a75c", null, "#5e6836", "#5e6836", "#d29641", "#d29641", "#ffb347", "#f4c076", "#f4c076", "#ffb347", "#d29641", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffecd1", "#ffecd1", "#d29641", "#d29641", "#d29641", "#ffb347", "#ffb347", "#d29641", "#a2a75c", "#5e6836", "#5e6836", "#5e6836", "#393f21", "#d29641", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, "#e1c5c1", "#ffe3e0", "#ffe3e0", "#ffe3e0", null, null, null, "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#ffecd1", "#ffecd1", "#d29641", "#ffb347", "#f4c076", "#f4c076", "#d29641", "#5e6836", "#5e6836", "#5e6836", "#5e6836", "#393f21", "#393f21", "#d29641", "#ffb347", "#ffb347", "#f4c076", "#ffb347", "#a2a75c", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, "#e1c5c1", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", null, null, "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#ffecd1", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#5e6836", "#5e6836", "#5e6836", "#5e6836", "#a2a75c", "#393f21", "#393f21", "#e1c5c1", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#d29641", "#d29641", null, "#d29641", "#d29641", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, "#ffe3e0", "#d2ba9d", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#d2ba9d", "#ffe3e0", "#d29641", "#d29641", "#ffb347", "#f4c076", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#393f21", "#5e6836", "#a2a75c", "#393f21", "#393f21", "#393f21", "#393f21", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, "#e1c5c1", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#d2ba9d", "#f0d4d0", "#d2ba9d", "#d2ba9d", "#ffe3e0", "#ffe3e0", null, "#d29641", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#393f21", "#393f21", "#393f21", "#5e6836", "#5e6836", "#5e6836", "#e1c5c1", "#e1c5c1", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#ffb347", "#ffb347", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, "#e1c5c1", "#ffe3e0", "#ffe3e0", "#f0d4d0", "#d2ba9d", "#a98047", "#a98047", "#f0d4d0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#393f21", "#d29641", "#d29641", "#ffb347", "#f4c076", "#f4c076", "#d29641", "#ffb347", "#ffb347", "#393f21", "#393f21", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#d2ba9d", "#f0d4d0", "#d2ba9d", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffb347", "#ffb347", "#ffb347", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, "#ffe3e0", "#ffe3e0", "#f0d4d0", "#a98047", "#e5ac5d", "#e5ac5d", "#f0d4d0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#393f21", "#393f21", "#d29641", "#d29641", "#ffb347", "#d29641", "#ffb347", "#f4c076", "#393f21", "#393f21", "#393f21", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#f0d4d0", "#a98047", "#e5ac5d", "#a98047", "#f0d4d0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffb347", "#ffb347", "#d29641", "#d29641", null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, "#ffe3e0", "#ffe3e0", "#f0d4d0", "#a98047", "#a98047", "#f0d4d0", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#393f21", "#393f21", "#393f21", "#393f21", "#d29641", "#d29641", "#d29641", "#d29641", "#393f21", "#393f21", "#393f21", "#ffb347", "#ffb347", "#ffecd1", "#ffb347", "#d29641", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#d2ba9d", "#e5ac5d", "#e5ac5d", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffb347", "#ffb347", "#d29641", "#b68b5d", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, "#f0d4d0", "#d2ba9d", "#d2ba9d", "#f0d4d0", "#ffe3e0", "#d2ba9d", "#393f21", "#393f21", "#5e6836", "#758052", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#ffb347", "#ffb347", "#f4c076", "#ffecd1", "#ffb347", "#d29641", "#e1c5c1", "#e1c5c1", "#d2ba9d", "#f0d4d0", "#e5ac5d", "#a98047", "#f0d4d0", "#d2ba9d", "#ffe3e0", "#ffb347", "#ffb347", "#d29641", "#d29641", "#b68b5d", "#b68b5d", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, "#d2ba9d", "#f0d4d0", "#f0d4d0", "#f0d4d0", "#ffe3e0", "#393f21", "#393f21", "#758052", "#d29641", "#d29641", "#d29641", "#5e6836", "#5e6836", "#5e6836", "#a2a75c", "#393f21", "#393f21", "#393f21", "#ffb347", "#f4c076", "#ffb347", "#ffb347", "#ffecd1", "#d29641", "#ffb347", "#e1c5c1", "#ffe3e0", "#f0d4d0", "#f0d4d0", "#d2ba9d", "#f0d4d0", "#ffe3e0", "#ffe3e0", "#d29641", "#d29641", "#d29641", "#b68b5d", "#b68b5d", "#d8b186", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#b68b5d", "#b68b5d", "#ffe3e0", "#393f21", "#393f21", "#393f21", "#d29641", "#ffb347", "#ffecd1", "#d29641", "#d29641", "#d29641", "#d29641", "#d29641", "#5e6836", "#393f21", "#393f21", "#ffb347", "#ffb347", "#f4c076", "#f4c076", "#ffb347", "#ffecd1", "#d29641", "#e1c5c1", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#ffe3e0", "#d29641", "#d29641", "#393f21", "#b68b5d", "#b68b5d", "#d8b186", "#d8b186", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#b68b5d", "#b68b5d", "#393f21", "#4f582d", "#4f582d", "#393f21", "#d29641", "#ffb347", "#f4c076", "#ffecd1", "#ffb347", "#d29641", "#ffb347", "#ffb347", "#d29641", "#a2a75c", "#393f21", "#ffb347", "#ffb347", "#f4c076", "#f4c076", "#ffb347", "#ffb347", "#d29641", "#ffb347", "#ffb347", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#5e6836", "#d29641", "#d29641", "#393f21", "#b68b5d", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#b68b5d", "#e2c4a2", "#b68b5d", "#393f21", "#393f21", "#393f21", "#d29641", "#ffb347", "#ffb347", "#f4c076", "#ffecd1", "#d29641", "#ffb347", "#ffb347", "#d29641", "#5e6836", "#393f21", "#393f21", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#d29641", "#d29641", "#ffb347", "#ffb347", "#a2a75c", "#758052", "#5e6836", "#4f582d", "#4f582d", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#e2c4a2", "#e2c4a2", "#b68b5d", "#b68b5d", "#393f21", "#d29641", "#ffb347", "#ffb347", "#ffb347", "#ffb347", "#ffecd1", "#e1c5c1", "#e1c5c1", "#e1c5c1", "#5e6836", "#393f21", "#393f21", "#393f21", "#ffb347", "#ffb347", "#d29641", "#d29641", "#ffb347", "#ffb347", "#a2a75c", "#a2a75c", "#758052", "#4f582d", "#4f582d", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#b68b5d", "#b68b5d", "#b68b5d", "#ffb347", "#e1c5c1", "#e1c5c1", "#e1c5c1", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#393f21", "#393f21", "#393f21", "#393f21", "#ffb347", "#d29641", "#ffb347", "#393f21", "#393f21", "#a2a75c", "#758052", "#4f582d", "#4f582d", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#e1c5c1", "#d2ba9d", "#ffe3e0", "#ffe3e0", "#f0d4d0", "#ffe3e0", "#ffe3e0", "#d2ba9d", "#ffe3e0", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#4f582d", "#4f582d", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#ffe3e0", "#d2ba9d", "#f0d4d0", "#f0d4d0", "#f0d4d0", "#d2ba9d", "#d2ba9d", "#ffe3e0", "#e1c5c1", "#393f21", "#a2a75c", "#393f21", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#5e6836", "#4f582d", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#d7b189", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#ffe3e0", "#a98047", "#e5ac5d", "#e5ac5d", "#f0d4d0", "#f0d4d0", "#ffe3e0", "#e1c5c1", "#393f21", "#a2a75c", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#a98047", "#a98047", "#a98047", "#f0d4d0", "#f0d4d0", "#e1c5c1", "#e1c5c1", "#a2a75c", "#a2a75c", "#ffe3e0", "#f0d4d0", "#f0d4d0", "#a98047", "#ffe3e0", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#e2c4a2", "#ffe3e0", "#a98047", "#ffe3e0", "#d2ba9d", "#ffe3e0", "#e1c5c1", "#ffe3e0", "#393f21", "#a2a75c", "#ffe3e0", "#f0d4d0", "#f0d4d0", "#e5ac5d", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#ffe3e0", "#d2ba9d", "#a98e6d", "#e1c5c1", "#ffe3e0", "#a2a75c", "#a2a75c", "#ffe3e0", "#ffe3e0", "#e5ac5d", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#966e43", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#d2ba9d", "#d2ba9d", "#4f582d", "#4f582d", "#4f582d", "#4f582d", "#4f582d", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#caa072", "#caa072", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#393f21", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#393f21", "#393f21", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#caa072", "#caa072", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#eed8be", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#eed8be", "#eed8be", "#e2c4a2", "#b68b5d", "#ffe3e0", "#ffe3e0", "#ffe3e0", "#393f21", "#b68b5d", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#eed8be", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#d1a87a", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#eed8be", "#e2c4a2", "#e2c4a2", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#caa072", "#caa072", "#d8b186", "#d8b186", "#d8b186", "#d8b186", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#d8b186", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#caa072", "#caa072", "#d8b186", "#d8b186", "#caa072", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#e2c4a2", "#b68b5d", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#b68b5d", "#caa072", "#d8b186", "#caa072", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#e2c4a2", "#b68b5d", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#b68b5d", "#caa072", "#caa072", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#966e43", "#e6c198", "#e6c198", "#e6c198", "#e2c4a2", "#b68b5d", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#b68b5d", "#caa072", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#d7b189", "#e6c198", "#d8b186", "#b68b5d", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#f6e7d1", "#b68b5d", "#caa072", "#caa072", "#b68b5d", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#d1a87a", "#d8b186", "#d8b186", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#b68b5d", "#d8b186", "#b35754", "#b35754", "#b35754", "#c1665c", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b68b5d", "#d1a87a", "#d1a87a", "#d1a87a", "#d8b186", "#b68b5d", "#d8b186", "#d8b186", "#d8b186", "#b68b5d", "#d8b186", "#d8b186", "#b35754", "#c1746c", "#f2ceca", "#f2ceca", "#f2ceca", "#c1746c", "#c1665c", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#b35754", "#b35754", "#b35754", "#c1665c", "#b68b5d", "#d8b186", "#b68b5d", "#d8b186", "#d8b186", "#b35754", "#c1746c", "#f5b4ab", "#8d4038", "#b35754", "#f5b4ab", "#f5b4ab", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#ad745c", "#b35754", "#f2ceca", "#f5b4ab", "#f5b4ab", "#c1746c", "#c1746c", "#8d4038", "#d8b186", "#b68b5d", "#d8b186", "#b35754", "#c1746c", "#f5b4ab", "#8d4038", "#b35754", "#b35754", "#b35754", "#c1746c", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#c1665c", "#f5b4ab", "#c1665c", "#b35754", "#b35754", "#b35754", "#c1746c", "#8d4038", "#8d4038", "#8d4038", "#8d4038", "#8d4038", "#f5b4ab", "#8d4038", "#b35754", null, null, "#b35754", "#c1746c", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#f5b4ab", "#b35754", null, null, "#8d4038", "#8d4038", "#8d4038", "#8d4038", "#f2ceca", "#f5b4ab", "#8d4038", "#8d4038", "#8d4038", "#b35754", "#b35754", "#b35754", "#b35754", "#c1746c", "#c1665c", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#c1665c", "#f2ceca", "#f5b4ab", "#b35754", "#b35754", "#b35754", "#c1746c", "#8d4038", "#8d4038", "#f5b4ab", "#c1746c", "#8d4038", "#c1746c", "#f5b4ab", "#f5b4ab", "#f5b4ab", "#f5b4ab", "#f5b4ab", "#c1665c", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#c1665c", "#f5b4ab", "#f5b4ab", "#c1746c", "#c1746c", "#8d4038", "#8d4038", "#b35754", "#b35754", "#8d4038", "#c1746c", "#b35754", "#b35754", "#c1665c", "#b35754", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#b35754", "#c1665c", "#8d4038", "#8d4038", "#8d4038", "#8d4038", "#8d4038", "#8d4038", "#c1746c", "#c1746c", "#c1665c", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#8d4038", "#8d4038", "#c1746c", "#c1746c", "#b35754", "#ad745c", "#b35754", "#b35754", "#f5b4ab", "#8d4038", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#f2ceca", "#f2ceca", "#c1746c", "#b35754", "#e2c4a2", "#d8af83", "#ad745c", "#b35754", "#c1746c", "#f2ceca", "#f5b4ab", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#f2ceca", "#f2ceca", "#f5b4ab", "#b35754", "#e2c4a2", "#d8af83", "#d8af83", "#d8b186", "#ad745c", "#b35754", "#c1746c", "#f2ceca", "#f5b4ab", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#f2ceca", "#f2ceca", "#f2ceca", "#f5b4ab", "#b35754", "#e2c4a2", "#e2c4a2", "#d8af83", "#d8af83", "#e2c4a2", "#d8b186", "#ad745c", "#ad745c", "#b35754", "#c1746c", "#c1746c", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#f5b4ab", "#f5b4ab", "#b35754", "#ad745c", "#e2c4a2", "#d8af83", "#d8af83", "#d8af83", "#e2c4a2", "#d8b186", "#d8b186", "#ad745c", "#ad745c", "#b35754", "#f5b4ab", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#b35754", "#b35754", "#b35754", "#393f21", "#393f21", "#ad745c", "#ad745c", "#ad745c", "#ad745c", "#ad745c", "#ad745c", "#ad745c", "#4f582d", null, "#b35754", "#b35754", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#393f21", "#4b5521", "#393f21", "#4b5521", "#5e6836", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#4b5521", "#a2a75c", "#5e6836", "#4f582d", "#393f21", "#5e6836", "#a2a75c", "#4b5521", "#a2a75c", "#393f21", "#393f21", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#a2a75c", "#4b5521", "#5e6836", null, "#4b5521", "#a2a75c", "#5e6836", "#a2a75c", "#4b5521", "#393f21", "#4b5521", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#a2a75c", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, "#4b5521", null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
    [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null],
];


/* ============================================================
   CANVAS
   ============================================================ */

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");


/* ============================================================
   PREPARAR LA LISTA DE PÍXELES A DIBUJAR
   ============================================================

   Antes se recorría CADA una de las 4096 casillas de la
   cuadrícula (64x64), incluyendo las vacías, y se esperaba
   TIEMPO_ENTRE_PIXELES antes de pasar a la siguiente, tuviera
   color o no. Eso hacía que, si tu dibujo tiene muchos huecos
   vacíos arriba o a los costados, pasaran varios segundos
   sin que se viera absolutamente nada.

   Ahora, en cambio, armamos de una vez la lista de los
   píxeles que SÍ tienen color, y solo esperamos entre esos.
   Así el primer color aparece casi de inmediato.
   ============================================================ */

function prepararListaDePixeles() {

    const lista = [];

    for (let y = 0; y < ALTO; y++) {

        const fila = PIXELS[y];

        if (!fila) {
            continue;
        }

        for (let x = 0; x < ANCHO; x++) {

            const color = fila[x];

            if (color) {
                lista.push({ x: x, y: y, color: color });
            }

        }

    }

    return lista;

}


/* ============================================================
   ⭐ ORDEN ALEATORIO DE LOS PÍXELES
   ============================================================

   Baraja la lista de píxeles (algoritmo Fisher-Yates) para
   que no aparezcan en orden de fila por fila, sino en un
   orden distinto cada vez que se dibuja.
   ============================================================ */

function barajarLista(lista) {

    for (let i = lista.length - 1; i > 0; i--) {

        const j = Math.floor(Math.random() * (i + 1));

        const temp = lista[i];
        lista[i] = lista[j];
        lista[j] = temp;

    }

    return lista;

}


/* ============================================================
   ⭐ ESPERA ALEATORIA ENTRE PÍXELES
   ============================================================

   Este "contador" calcula, cada vez que se llama, una
   cantidad de milisegundos aleatoria distinta (entre
   TIEMPO_ENTRE_PIXELES_MIN y TIEMPO_ENTRE_PIXELES_MAX) que
   se usa como espera antes de dibujar el siguiente píxel.
   ============================================================ */

function tiempoAleatorioEntrePixeles() {

    return Math.floor(

        Math.random() *

        (TIEMPO_ENTRE_PIXELES_MAX - TIEMPO_ENTRE_PIXELES_MIN + 1)

    ) + TIEMPO_ENTRE_PIXELES_MIN;

}


/* ============================================================
   ⭐ CONTROL PARA EVITAR QUE SE REINICIE LA ANIMACIÓN
   ============================================================

   Esta era la causa más probable de que "no se viera la
   animación": cada evento "resize" llamaba de nuevo a
   dibujarPixeles(), lo cual reiniciaba canvas.width (¡eso
   BORRA todo lo dibujado!) y volvía a empezar desde cero,
   mientras el ciclo anterior seguía corriendo por su cuenta.
   En el celular (o al cargar la página), el navegador puede
   disparar "resize" varias veces seguidas, así que la
   animación se reiniciaba una y otra vez sin parar.

   Con "generacion" le damos a cada llamada de
   dibujarPixeles() un número. Si empieza una llamada nueva,
   las animaciones de llamadas viejas se detienen solas al
   notar que su número ya no es el actual.
   ============================================================ */

let generacionActual = 0;


function dibujarPixeles() {

    generacionActual++;
    const miGeneracion = generacionActual;

    canvas.width =
        window.innerWidth;

    canvas.height =
        window.innerHeight;

    ctx.clearRect(

        0,
        0,
        canvas.width,
        canvas.height

    );

    const escala = Math.min(

        window.innerWidth / ANCHO,

        window.innerHeight / ALTO

    );

    const offsetX = (

        window.innerWidth -

        ANCHO * escala

    ) / 2;

    const offsetY = (

        window.innerHeight -

        ALTO * escala

    ) / 2;

    const lista = barajarLista(prepararListaDePixeles());

    let indice = 0;

    function siguiente() {

        // Si mientras tanto empezó otra animación más nueva
        // (por ejemplo, por un resize), esta se detiene sola.
        if (miGeneracion !== generacionActual) {
            return;
        }

        if (indice >= lista.length) {
            return;
        }

        const p = lista[indice];

        ctx.fillStyle = p.color;

        ctx.fillRect(

            offsetX + p.x * escala,

            offsetY + p.y * escala,

            escala,

            escala

        );

        indice++;

        setTimeout(

            siguiente,

            tiempoAleatorioEntrePixeles()

        );

    }

    siguiente();

}


/* ============================================================
   ⭐ VALIDACIÓN DEL NOMBRE Y FLUJO DE PANTALLAS
   ============================================================

   1) El visitante escribe su nombre y presiona "Continuar"
      (con el mouse o con la tecla Enter).
   2) Si el nombre (sin importar mayúsculas/minúsculas ni
      espacios extra) es "sally" o "marie", se muestra la
      pantalla de bienvenida y luego el dibujo.
   3) Si no, se muestra el mensaje de error y el dibujo
      nunca se revela.
   ============================================================ */

const pantallaInicio = document.getElementById("inicio");
const pantallaBienvenida = document.getElementById("bienvenida");
const mensajeBienvenida = document.getElementById("mensajeBienvenida");
const campoNombre = document.getElementById("nombre");
const botonContinuar = document.getElementById("boton");
const mensajeError = document.getElementById("error");

let regaloDesbloqueado = false;

function capitalizar(texto) {

    return texto.charAt(0).toUpperCase() + texto.slice(1);

}

function intentarContinuar() {

    const valor = campoNombre.value.trim().toLowerCase();

    if (NOMBRES_PERMITIDOS.includes(valor)) {

        mensajeError.style.display = "none";

        pantallaInicio.style.display = "none";

        mensajeBienvenida.textContent =
            "Bienvenida "  + capitalizar (valor) + "! Este es tu regalo de parte de A...";

        pantallaBienvenida.style.display = "flex";

        setTimeout(function() {

            pantallaBienvenida.style.display = "none";

            canvas.style.display = "block";

            regaloDesbloqueado = true;

            dibujarPixeles();

        }, 4500);

    } else {

        mensajeError.style.display = "block";

    }

}    
botonContinuar.addEventListener("click", intentarContinuar);

campoNombre.addEventListener("keydown", function(evento) {
    if (evento.key === "Enter") {
        evento.preventDefault();
        botonContinuar.classList.add("presionado");
        setTimeout(function() {
            botonContinuar.classList.remove("presionado");
            intentarContinuar();
        }, 100);
    }
});


/* ============================================================
   CAMBIO DE TAMAÑO DE LA VENTANA
   ============================================================

   Se agrupan varios eventos "resize" seguidos (algo normal
   al abrir la página, sobre todo en el celular) en uno solo,
   esperando 200ms después del último antes de volver a
   dibujar — así no se reinicia la animación en cadena.
   ============================================================ */

let temporizadorResize = null;

window.addEventListener(

    "resize",

    function() {

        clearTimeout(temporizadorResize);

        temporizadorResize = setTimeout(

            function() {

                if (regaloDesbloqueado) {

                    dibujarPixeles();

                }

            },

            200

        );

    }

);

</script>

</body>

</html>
"""


@app.route("/")
def inicio():

    return render_template_string(HTML)


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000

    )
