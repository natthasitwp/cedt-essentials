---
title: Convolution integral และวิธี flip-and-shift
src: L05
minutes: 25
slides: 2–4
deck: L05
goal: หา \( y(t)=x(t)*h(t) \) ด้วยการพลิกและเลื่อน แล้วเขียนคำตอบแยกตามช่วงของ \( t \)
oneline: นิยาม convolution และการหาด้วยกราฟ
cheat:
  - "\( y(t)=\int_{-\infty}^{\infty} x(\tau)\,h(t-\tau)\,d\tau \)"
  - "rect กว้าง 1 * rect กว้าง 1 = สามเหลี่ยมกว้าง 2 สูง 1"
sources:
  - "[MIT OCW 6.003](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) บทเรื่อง convolution มีตัวอย่างกราฟเพิ่ม"
---
## นิยาม

::slide 2 | สไลด์ 2: LTI system, impulse response และสูตร convolution integral | ดูสูตรตรงกลางสไลด์

:::def สูตร · สไลด์ 2
$$ y(t) = \int_{-\infty}^{\infty} x(\tau)\, h(t-\tau)\, d\tau $$
:::

ตัวแปร *τ* คือแกนที่เราอินทิเกรต ส่วน \( t \) คือ **ตำแหน่งที่เลื่อน** \( h \) ไป สังเกต `x_1 * y_2` ต้องไม่กลายเป็นตัวเอียง

## ลองเลื่อนเอง

::widget convolution {"x": "rect(0,1)", "h": "rect(0,1)", "range": [-2, 4], "t": 0.5}

:::predict ถ้า \( t = 1.5 \) พื้นที่ที่ซ้อนกันเท่าไร?
ซ้อนกันช่วง \( [0.5, 1] \) ยาว 0.5 จึงได้ \( y(1.5) = 0.5 \)
:::

:::warn
ลืมพลิก \( h \) เป็น \( h(-\tau) \) ก่อนเลื่อน
:::

| ช่วง | y(t) |
|---|---|
| \( 0 \le t < 1 \) | \( t \) |
| \( 1 \le t < 2 \) | \( 2-t \) |

:::quiz
? num | slide 4 | หา \( y(1.5) \) ของ rect * rect
answer: 0.5
hint: ดูช่วงที่ซ้อนกัน
sol: ซ้อนกันบน \( [0.5,1] \) จึงได้ 0.5

? mc | ผลของ rect * rect มีรูปร่างแบบใด
- สี่เหลี่ยม
- [x] สามเหลี่ยม
- เอกซ์โพเนนเชียล
sol: ความกว้างรวมเป็น 2 และขึ้นแล้วลงเป็นเส้นตรง
  จึงเป็นสามเหลี่ยม

? think | อธิบายว่าทำไมต้องพลิก \( h \)
sol: เพราะสูตรใช้ \( h(t-\tau) \)
:::
