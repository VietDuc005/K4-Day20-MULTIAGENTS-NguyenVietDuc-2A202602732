# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin sinh viên và cấu hình

- Họ tên: Nguyễn Viết Đức
- Mã sinh viên: 2A202602732
- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: OpenRouter (`openai/gpt-4o-mini`), nhiệt độ `0`, `recursion_limit = 60`.
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Python 3.11 (`.venv`), Windows 11, chạy trực tiếp trên host.
- Số lần chạy tác vụ đã dùng / ngân sách: 0 / 30
- Commit của tag `freeze`:

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): Subagents sẽ đạt điểm tương đương hoặc chỉ nhỉnh hơn nhẹ baseline trên tác vụ đánh giá nhưng tiêu tốn token cao hơn đáng kể (ước tính tăng 1.5 - 2.5 lần). Căn cứ: subagent bị cô lập ngữ cảnh (context-isolated), chỉ nhận chỉ đạo tóm tắt từ tác tử chính nên dễ thiếu sót các quy tắc ẩn; đồng thời các nghiên cứu về multi-agent (như nghiên cứu của Anthropic về multi-agent research systems) chỉ ra đa tác tử tốn nhiều token và có thể gặp lỗi phân rã nhiệm vụ nếu prompt ủy quyền không bao quát đủ ràng buộc.
- H2 (skills-auto so với baseline): Skills-auto sẽ đạt điểm cao hơn baseline trên tác vụ học (đặc biệt ở các check quy ước tổ chức Acme như type annotations, changelog, regression tests), nhưng trên tác vụ đánh giá mức độ cải thiện sẽ thấp hơn do xuất hiện các quy ước mới chưa từng học. Căn cứ: nghiên cứu SkillsBench và SkillEvolBench chỉ ra skill do mô hình tự sinh có xu hướng thích nghi tốt trên tập học nhưng gặp hiện tượng quá khớp (overfitting ở tầng context) và khó chuyển giao toàn vẹn sang các bài toán có ràng buộc mới.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm trung bình của tất cả các điều kiện trên tác vụ học sẽ cao hơn điểm trên tác vụ đánh giá. Căn cứ: tác vụ đánh giá không có phản hồi `detail` (detail = '') khi kiểm tra thất bại, dữ liệu bẩn hơn và có bổ sung thêm các quy ước tổ chức mới mà tác tử chưa từng quan sát trong quá trình học.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử Deep Agents mặc định có 9 công cụ: 7 công cụ tệp (`ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`), 1 công cụ shell (`execute`), và 1 công cụ đa tác tử (`task`). Công cụ cho phép thực thi lệnh shell trực tiếp là `execute`.
2. Mô tả của công cụ `task` cho biết subagent `general-purpose` được dùng để nghiên cứu các câu hỏi phức tạp, tìm kiếm tệp/nội dung và thực hiện các tác vụ nhiều bước, có đầy đủ công cụ như tác tử chính. Về ngữ cảnh, subagent hoàn toàn độc lập/không trạng thái (stateless by default): nó chỉ nhìn thấy duy nhất nội dung prompt mà tác tử chính truyền sang khi giao việc (không nhìn thấy ngữ cảnh lịch sử trước đó của tác tử chính) và trả về một bản báo cáo tóm tắt cuối cùng.
3. - Trích hướng dẫn hành vi từ mô tả công cụ `task`: *"Put full detail in the prompt and state exactly what it should return"* (và *"Tell the agent whether to create content, analyze, or only research, since it can't necessarily see the user's intent"*).
   - Trích hướng dẫn hành vi từ mô tả công cụ `execute`: *"Use absolute paths and avoid `cd` so the working directory stays stable"* (và *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail"*).

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `code-learn` | `rule_type_hints` | E. Vi phạm quy ước tổ chức | `detail: RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value.` |
| `code-learn` | `rule_regression_tests` | E. Vi phạm quy ước tổ chức | `detail: RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass.` |
| `code-learn` | `rule_changelog` | E. Vi phạm quy ước tổ chức | `detail: RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets).` |
| `code-learn` | `csv_quoting_follows_docstring` | A. Bỏ qua đặc tả | Tác tử ghép chuỗi thủ công thay vì format chuẩn: `to_csv_row returned 'Desk, large "oak",10.00,2'` |
| `code-learn` | `parse_price_all_formats` | D. Bỏ sót định dạng | Tác tử xử lý thiếu trường hợp số âm đóng mở ngoặc: `wrong for: ['(12.00)']` |
| `code-learn` | `discount_rounds_half_up` | B. Không kiểm chứng | Tác tử không đối chiếu quy tắc làm tròn nửa lên trong docstring: `wrong for: [('10.05', 10, '9.05')...]` |
| `data-learn` | `rule_clean_csv` | E. Vi phạm quy ước tổ chức | `detail: RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents...` |
| `logs-learn` | `valid_structure` | F. Báo cáo hoàn thành sai sự thật | Tác tử kết thúc phiên mà chưa hoàn thành ghi tệp: `FileNotFoundError: errors.json` |

Nhận xét: Nhóm lỗi chiếm đa số và làm mất điểm nặng nề nhất là **Nhóm E (Vi phạm quy ước tổ chức)**. Các quy ước này không xuất hiện trực tiếp trong phần đề bài ngắn gọn mà là chuẩn mực riêng của tổ chức (Acme). Một bộ Skill thủ tục (procedural skill) hoàn toàn có thể phòng ngừa triệt để nhóm lỗi này bằng cách cung cấp quy tắc định dạng và danh sách kiểm tra (checklist) bắt buộc ngay từ đầu.

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):
  1. `explorer`: Đóng vai trò khảo sát, đọc hiểu cấu trúc thư mục, README, docstrings, schema dữ liệu hoặc mẫu log; chế độ chỉ đọc, không sửa tệp.
  2. `implementer`: Đóng vai trò thực thi các thao tác sửa code, tính toán số liệu, xử lý file và chạy lệnh shell/test để báo cáo kết quả.
  3. `reviewer`: Đóng vai trò rà soát chất lượng độc lập, đối chiếu các file kết quả với yêu cầu đề bài và các trường hợp biên; không sửa tệp.
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):
  - `code-learn`: 0 lần.
  - `data-learn`: 0 lần.
  - `logs-learn`: 0 lần.
  - Nhận xét: Tác tử chính có xu hướng ưu tiên tự gọi trực tiếp các công cụ có sẵn (`glob`, `read_file`, `write_file`, `execute`) thay vì giao việc qua công cụ `task`. Điều này xảy ra do tác tử chính muốn duy trì toàn bộ ngữ cảnh trong bộ nhớ và tránh chi phí trễ khi giao việc cho subagent không trạng thái (stateless context).
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc): Không áp dụng do tác tử chính tự xử lý toàn bộ.
- Ảnh hưởng đến token và thời gian: Điều kiện `subagents` làm tăng số lượng token đầu vào (input tokens) do `system_prompt` phải nạp thêm định nghĩa chi tiết của 3 subagents (trên `code-learn` token tăng từ 168.5k lên 229.6k, thời gian thực thi tăng từ 72.9s lên 120.1s).

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do: Chạy 1 lần, sinh ra 3 skill hợp lệ trong `skills/auto/`. Không có skill nào bị xóa vì tất cả đều tuân thủ định dạng YAML, dưới 40 dòng và nắm bắt đúng các phản hồi quy ước.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `code-quality` | Rất tổng quát cho họ `code` (chuẩn hóa type hints, unit test độc lập, CHANGELOG) | Đúng, khớp chính xác các quy ước Acme được phản hồi từ bot đánh giá | 13 dòng. Description rõ ràng ("Use when writing or modifying code..."). `skills_read` = 1. |
| `error-handling` | Tổng quát cho các thao tác tệp và kiểm tra đường dẫn | Đúng, hướng dẫn kiểm tra sự tồn tại của file trước khi xử lý | 13 dòng. Description hướng hành động. `skills_read` = 0. |
| `procedural-clarity` | Tổng quát cho quy trình phân rã tác vụ và lập checklist | Đúng, hướng dẫn chia nhỏ bài toán và tự kiểm tra | 13 dòng. Description bao quát. `skills_read` = 0. |

Hiệu quả ở Phần 3.4 (thử nghiệm trên tác vụ học):
- Trên `code-learn`: `skills-auto` giúp điểm tăng gấp đôi từ 2/10 lên 4/10. Đặc biệt, số lượng tool calls giảm từ 63 xuống còn 12 calls, thời gian giảm từ 72.9s xuống 18.8s và lượng token tiêu thụ giảm ngoạn mục từ 168.5k xuống 34.1k (tiết kiệm gần 80% chi phí token).

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Bạn đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
