# oai.studio 站内优化方案 — W01

---

## 一、首页优化

### 1.1 Hero Banner CTA 文案优化

**当前文案：**
```
HANDMADE ARTISAN KEYCAPS DESIGNED TO BRING WARMTH TO EVERY KEYSTROKE.
TINY COMPANIONS FOR YOUR CREATIVE SPACE
[DISCOVER PRODUCTS]
```

**优化方案A（强调稀缺性）：**
```
HANDMADE IN KYOTO, FINISHED BY HAND.
TINY COMPANIONS FOR YOUR KEYBOARD — LIMITED DROPS.
[SHOP THE COLLECTION →]
```

**优化方案B（强调情感价值）：**
```
WHEN WAS THE LAST TIME YOUR KEYBOARD MADE YOU SMILE?
MEET THE CREAM BEAR — HANDMADE IN KYOTO.
[FIND YOUR COMPANION →]
```

**优化方案C（强调社会证明）：**
```
10,000+ DESK SPACES WORLDWIDE CHOSE A TINY COMPANION.
HANDMADE ARTISAN KEYCAPS FROM KYOTO.
[JOIN THE COLLECTION →]
```

**推荐：方案B** — 情感钩子最强，与品牌调性最契合

### 1.2 倒计时器修复

**问题：** 倒计时显示 00:00:00:00，已失效，严重损害信任感

**修复方案：**
- 选项1：移除倒计时，改为"限量发售"标签
- 选项2：更新为真实的下次上新时间
- 选项3：改为"已有 X 人加入"的社会证明数字

**推荐：选项3** — 用真实数据替代失效倒计时

### 1.3 首页 SEO Meta 优化

**当前 Title：** Oai Studio | Cute Artisan Keycaps & Desk Companions

**优化后 Title：** Oai Studio — Handmade Artisan Keycaps from Kyoto | Kawaii Keyboard Companions

**Meta Description（新增）：**
```
Oai Studio crafts handmade artisan keycaps in Kyoto, Japan. 
Cream Bear, Magic Cat & more — 3D printed, hand-finished, ships worldwide. 
10,000+ happy desks. First order: 10% OFF + mystery gift.
```

---

## 二、产品页优化

### 2.1 产品描述 CTA 区块（所有产品页末尾添加）

```html
<!-- 在产品描述末尾添加 -->
<div class="product-cta-blog">
  <h3>Want to see more tiny companions?</h3>
  <p>Read our studio journal to discover the story behind each piece.</p>
  <a href="/blogs/studio-note">Visit the Studio Journal →</a>
</div>
```

### 2.2 产品页 Title 规范化

**当前格式：** `[产品名] ｜ Oai Studio ｜ Artisan Mechanical Keycap`

**问题：** 使用全角竖线 `｜`，部分搜索引擎显示异常

**优化格式：** `[产品名] — Artisan Keycap | Oai Studio`

**示例：**
- 当前：`Pudding Boat the Cream Bear ｜ Oai Studio ｜ Artisan Mechanical Keycap`
- 优化：`Cream Bear "Pudding Boat" Artisan Keycap — 3D Printed & Hand-Finished | Oai Studio`

---

## 三、集合页优化

### 3.1 集合页描述文案（全部缺失，需新增）

**Artisan Keycaps 集合页描述：**
```
Discover our full collection of handmade artisan keycaps — each one 
3D printed, hand-finished, and designed to bring a little warmth to 
your keyboard. From the Cream Bear series to our Special Keys collection, 
every piece is crafted in small batches at our Kyoto studio.

Compatible with Cherry MX switches. Ships worldwide.
```

**Cream Bear 集合页描述：**
```
The Cream Bear is our signature series — a tiny kawaii companion 
inspired by soft, sweet moments in everyday life. Available in 
Toast, Lemonade, Grape Soda, Ramune, and more colorways.

Each bear is hand-finished and packed in our signature gift box.
```

---

## 四、博客文章优化

### 4.1 现有3篇文章改版方案

**文章1：Why I Wanted Softer Keycaps**
- 当前字数：约 300 词（过短）
- 目标字数：800-1000 词
- 需要添加：
  - 制作工艺详细描述（300词）
  - 产品推荐区块（内链到 Cream Bear 系列）
  - 结尾 CTA："Start your collection →"

**文章2：A Day in the Studio**
- 当前字数：约 200 词（极短）
- 目标字数：800 词
- 需要添加：
  - 一天工作流程详细描述
  - 工作室照片（带 ALT 标签）
  - 产品内链

**文章3：How Little Characters Become Companions**
- 当前字数：约 400 词
- 目标字数：1000 词
- 需要添加：
  - 每个角色系列的故事
  - 产品内链（每个系列链接到对应集合页）

### 4.2 博客文章末尾标准 CTA 模板

```
---

**Ready to find your tiny companion?**

Browse the full collection at [oai.studio/collections/artisan-keycaps](link).
First order comes with 10% off + a mystery gift from our studio.

[Shop Artisan Keycaps →]
```

---

## 五、转化漏斗优化优先级

| 优化项 | 位置 | 难度 | 预期转化提升 | 优先级 |
|--------|------|------|------------|--------|
| Hero CTA 文案 | 首页 Banner | 低 | +5-10% | P0 |
| 倒计时器修复 | 首页 | 低 | +3-5% | P0 |
| 博客文章产品 CTA | 3篇博客 | 低 | +2-5% | P0 |
| 集合页描述文案 | 所有集合页 | 中 | SEO+转化 | P1 |
| 产品页 Title 规范化 | 所有产品页 | 中 | SEO | P1 |
| 首页 Meta Description | 首页 | 低 | CTR+20% | P0 |
