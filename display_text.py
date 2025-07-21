DESCRIPTIONS = {
    "English": {
        "sidebar": """
## MOS Survey Instructions

------

**What is MOS?**

MOS (Mean Opinion Score) is a simple method to rate audio quality. In this survey, you'll listen to speech samples and rate them based on:

1. **Naturalness:** How natural is the generated speech compared to actual human speech?
2. **Intelligibility:** How clearly are the words in the generated speech compared to the actual transcription?
3. **Similarity:** How closely does the synthesized speech match a real (reference) voice?

------

**How to Rate:**

- **Step 1:** Enter your ID. The **Set ID** button becomes clickable when you enter a valid ID.
- **Step 2:** Listen to the audio sample.
- **Step 3:** Use the radio buttons to rate each aspect.
- **Step 4:** Click **Submit** to save your rating and move to the next sample.

------

**Additional Tips:**
- Use headphones in a quiet environment for best audio evaluation.
- Only "Submit" button can save your rating. "Back" and "Next" buttons can't.

------

***Thank you for participating in our MOS survey!***
        """,
        "naturalness_guidelines": """
<div style="font-size: 16px;">
    Listen to the speech sample and assess the quality of the audio based on <u><b>how close it is to natural speech</b></u> on a scale of 1 to 5.
</div>
        """,
        "intelligibility_guidelines": """
<div style="font-size: 16px;">
    Listen to the speech sample and assess <u><b>how clearly and accurately the spoken content is conveyed</b></u> on a scale of 1 to 5. Your rating should reflect how easily the words can be understood compared to the provided transcription. You <b style='color:red;'>should NOT</b> judge the naturalness of the voice or the speaker’s identity. Instead, focus solely on the clarity of the spoken words. <b>If there is background noise (e.g., static, hiss, or other unwanted artifacts) that affects your ability to understand the words, factor this into your evaluation.</b>
</div>
        """,
        "similarity_guidelines": """
<div style="font-size: 16px;">
    Listen to the speech samples and rate the <u><b>speaker similarity</b></u> between them on a scale of 1 to 5. Your rating should reflect your evaluation of how close the voices of the two speakers sound. You <b style='color:red;'>should NOT</b> judge the accent, content, grammar, expressiveness, or audio quality of the two voices. Instead, just focus on the similarity of the speakers to one another.
</div>
        """,
        "naturalness_table": """
| Score             | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| **5 - Excellent** | Speech sounds completely natural and like a real person.          |
| **4 - Good**      | Mostly natural with minor robotic artifacts.                      |
| **3 - Fair**      | A mix of natural and artificial characteristics.                  |
| **2 - Poor**      | Mostly unnatural with noticeable robotic cues.                    |
| **1 - Bad**       | Completely artificial and very robotic.                           |
        """,
        "intelligibility_table": """
| Score             | Description                           |
|-------------------|---------------------------------------|
| **5 - Excellent** | Perfect understanding without any effort. |
| **4 - Good**      | Easy to understand with minimal effort.  |
| **3 - Fair**      | Understandable with some effort.           |
| **2 - Poor**      | Difficult to understand.                   |
| **1 - Bad**       | Impossible to understand.                  |
        """,
        "similarity_table": """
| Score             | Description                           |
|-------------------|---------------------------------------|
| **5 - Excellent** | Sounds exactly like the reference voice.    |
| **4 - Good**      | Very similar to the reference voice.        |
| **3 - Fair**      | Somewhat similar to the reference voice.      |
| **2 - Poor**      | Different from the reference voice.           |
| **1 - Bad**       | Completely different from the reference voice.|
        """,
        "language_toggle": "Uncheck to see Vietnamese Guidelines"
    },
    "Vietnamese": {
        "sidebar": """
## Hướng dẫn đánh giá MOS

------

**MOS là gì?**

MOS (Mean Opinion Score) là phương pháp đơn giản để đánh giá chất lượng âm thanh. Trong khảo sát này, bạn sẽ nghe các mẫu giọng nói và chấm điểm trên các tiêu chí sau:

1. **Độ tự nhiên:** Giọng nói được tạo ra có tự nhiên như giọng nói con người không?
2. **Độ rõ ràng:** Các từ trong giọng nói được tạo ra có dễ nghe và chính xác so với bản phiên âm không?
3. **Độ giống nhau:** Giọng nói tổng hợp có giống với giọng nói gốc không?

------

**Cách đánh giá:**

- **Bước 1:** Nhập ID của bạn. Nút **Set ID** sẽ click được khi bạn nhập ID hợp lệ.
- **Bước 2:** Nghe mẫu âm thanh.
- **Bước 3:** Sử dụng các nút chọn để chấm điểm cho từng tiêu chí.
- **Bước 4:** Nhấn **Submit** để lưu đánh giá và chuyển sang mẫu tiếp theo.

------

**Mẹo:**
- Hãy sử dụng tai nghe và chọn không gian yên tĩnh để có đánh giá chính xác nhất.
- Chỉ có nút "Submit" mới có thể lưu đánh giá của bạn. Nút "Back" và "Next" không thể.

------

***Cảm ơn bạn đã tham gia khảo sát MOS của tụi mình!***
        """,
        "naturalness_guidelines": """
<div style="font-size: 16px;">
    Hãy nghe đoạn ghi âm và đánh giá chất lượng giọng nói dựa trên <u><b>mức độ tự nhiên</b></u> của nó (giống người thật hay không) theo thang điểm từ 1 đến 5.
</div>
        """,
        "intelligibility_guidelines": """
<div style="font-size: 16px;">
    Hãy nghe mẫu giọng nói và đánh giá <u><b>mức độ rõ ràng, chính xác của nội dung được truyền tải</b></u> theo thang điểm từ 1 đến 5. Điểm số của bạn nên phản ánh mức độ dễ hiểu của lời nói so với bản phiên âm được cung cấp, nghĩa là độ dễ dàng để nhận ra các từ được nói là các từ trong bản phiên âm. Bạn <b style='color:red;'>KHÔNG NÊN</b> đánh giá về sự tự nhiên của giọng nói hay giới tính/danh tính của người nói. Thay vào đó, hãy chỉ tập trung vào độ rõ ràng của các từ được nói ra. <b>Nếu có tạp âm (ví dụ: nhiễu, tiếng rè, hoặc các âm thanh không mong muốn khác) làm ảnh hưởng đến khả năng nghe hiểu, hãy cân nhắc đến cả yếu tố này khi chấm điểm.</b>
</div>
        """,
        "similarity_guidelines": """
<div style="font-size: 16px;">
    Hãy nghe hai đoạn âm thanh và đánh giá <u><b>mức độ giống nhau giữa hai giọng nói</b></u> theo thang điểm từ 1 đến 5. Điểm số của bạn nên phản ánh mức độ giống nhau của giọng nói giữa hai người trong hai đoạn âm thanh. Bạn <b style='color:red;'>KHÔNG NÊN</b> đánh giá về giọng điệu (accent), nội dung, ngữ pháp, cảm xúc, tốc độ nói, hay chất lượng âm thanh. Thay vào đó, hãy chỉ tập trung vào việc hai giọng nói có giống nhau hay không.
</div>
        """,
        "naturalness_table": """
| Điểm               | Mô tả                                                                   |
|--------------------|-------------------------------------------------------------------------|
| **5 - Excellent**   | Giọng nói nghe hoàn toàn tự nhiên, giống như một người thật.            |
| **4 - Good**        | Hầu như tự nhiên, chỉ có chút âm thanh máy móc không đáng kể. |
| **3 - Fair** | Kết hợp giữa đặc điểm tự nhiên và nhân tạo.                             |
| **2 - Poor**        | Chủ yếu nghe không tự nhiên, có nhiều dấu hiệu giọng máy.               |
| **1 - Bad**    | Hoàn toàn nhân tạo, nghe rõ ràng như giọng robot.                       |
        """,
        "intelligibility_table": """
| Điểm               | Mô tả                                                   |
|--------------------|---------------------------------------------------------|
| **5 - Excellent**   | Hoàn toàn hiểu được mà không cần bất kỳ sự cố gắng nào. |
| **4 - Good**        | Dễ hiểu, chỉ cần chú ý một chút.                            |
| **3 - Fair** | Có thể hiểu nhưng phải tập trung hơn.                   |
| **2 - Poor**        | Khó nghe, khó hiểu.                                     |
| **1 - Bad**    | Không thể hiểu được.                                    |
        """,
        "similarity_table": """
| Điểm               | Mô tả                                        |
|--------------------|----------------------------------------------|
| **5 - Excellent**   | Giống hệt giọng tham chiếu.                  |
| **4 - Good**        | Rất giống, chỉ có chút khác biệt nhỏ.        |
| **3 - Fair** | Có nét giống nhưng vẫn khác tương đối.       |
| **2 - Poor**        | Nghe khác khá nhiều so với giọng tham chiếu. |
| **1 - Bad**    | Không giống chút nào với giọng tham chiếu.   |
        """,
        "language_toggle": "Click chọn để xem hướng dẫn Tiếng Anh"
    }
}
