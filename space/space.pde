color black = color(0);
color white = color(255);
color currColor = white;
float lim = random(0.5);
float dPct = random(0.5, 0.9);

void setup() {
 size(400, 400, P3D);
 background(black);
 stroke(currColor);
 println("lim: " + lim);
 println("dPct: " + dPct);
}

String ccStr() {
  if (currColor == white) {
    return "white";
  } else {
    return "black";
  }
}

void flip() {
  if (currColor == black) {
    currColor = white;
  } else {
    currColor = black;
  }
  stroke(currColor);
  println("flip (" + ccStr() + ")");
}

boolean isCurr(color px) {
  float val = px & 0xFF;
  if (currColor == black) {
    return (val == 0);
  } else {
    return (val != 0);
  }
}

boolean shouldFlip() {
  loadPixels();
  int pxLen = pixels.length;
  float count = 0.0;
  for (int i = 0; i < pxLen; i++) {
    if (isCurr(pixels[i])) {
      count++;
    }
  }
  float pct = count / pxLen;
  return (pct >= lim);
}

int scaleFloat(float val, int min, int max) {
  float mult = abs(min) + abs(max);
  return int((val * mult) + min);
}

void draw() {
  int period = 1000;
  int adj = int(currColor == black) + 1;
  if ((frameCount % (period * adj) == 0) && shouldFlip()) flip();
  if (frameCount % 5000 == 0) {
    println("save");
    saveFrame("space.png");
  }
  float rawX = random(1);
  float rawY = random(1);
  float rawZ = random(1);
  int x = scaleFloat(rawX, 0, width);
  int y = scaleFloat(rawY, 0, height);
  int z = scaleFloat(rawZ, -100, 100);
  if ((currColor == black) || (random(1) >= dPct)) {
    point(x, y, z);
  }
}