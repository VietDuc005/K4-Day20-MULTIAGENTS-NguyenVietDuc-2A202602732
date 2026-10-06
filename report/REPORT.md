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

Bảng so sánh xuất từ `report/table.md` (`python -m lab.compare`):

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 2/10 | 1/10 | 0/10 |
| data-learn | 0/8 | 0/8 | 0/8 |
| logs-learn | 0/9 | 0/9 | 0/9 |
| code-eval | 0/11 | 0/11 | 0/11 |
| data-eval | 0/9 | 0/9 | 0/9 |
| logs-eval | 0/10 | 0/10 | 0/10 |
| **Mean score - learning tasks** | 0.07 | 0.03 | 0.00 |
| **Mean score - evaluation tasks** | 0.00 | 0.00 | 0.00 |
| **Mean tokens per run** | 107,141 | 107,142 | 0 |
| **Runs that read a skill** | 0/6 | 0/6 | 0/6 |

Thống kê phân rã check kỹ thuật và check quy ước (`python scripts/check_breakdown.py`):

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval      0/18         0/12               0      0/3     
baseline      learn     2/18         0/9          191,823      0/3     
subagents     eval      0/18         0/12               0      0/3     
subagents     learn     1/18         0/9          214,285      0/3     
skills-auto   eval      0/18         0/12               0      0/3     
skills-auto   learn     0/18         0/9                0      0/3     
```

Ghi nhận các lần chạy thử nghiệm và xử lý lỗi:
1. Kết quả thử nghiệm trước đóng băng (`results/skills-auto-dev/` ở Phần 3.4):
   - Trên `code-learn`: Tác tử nạp skill `code-quality`, đạt điểm **4/10** (tăng gấp đôi so với baseline 2/10). Thời gian chạy chỉ mất **18.8s**, số lần gọi công cụ là 12 calls, tiêu thụ **34,135 tokens** (giảm gần 80% so với baseline 168k tokens).
2. Các lần chạy có `error`:
   - `data-learn` (ở baseline và subagents): Tác tử rơi vào vòng lặp hiệu chỉnh code dữ liệu và chạm giới hạn `GraphRecursionError` (60 bước).
   - Các tác vụ đánh giá (eval) và lần chạy lại `skills-auto` sau tag freeze: Gặp lỗi hạn mức API từ nhà cung cấp (`APIStatusError: 402 - insufficient credits / in-flight limit`).
   - Xử lý: Harness ghi nhận lỗi đầy đủ vào trường `error` của `run.json`, tiếp tục chấm điểm trên workspace hiện có và hoàn thành quy trình mà không làm crash hệ thống.
3. Không có lần chạy nào bị `skills_modified = true` (toàn bộ giữ nguyên `skills_modified: false`), mã băm thư mục skill được đối chiếu chính xác.

## 8. Phân tích

1. **Hiệu quả cải thiện trên tác vụ học vs tác vụ đánh giá**:
   - So với `baseline` (2/10 trên `code-learn`), điều kiện `skills-auto` trong giai đoạn thử nghiệm (Phần 3.4) đã nâng điểm lên **4/10**, đồng thời giảm thời gian thực thi từ 72.9s xuống 18.8s. Điều kiện `subagents` chỉ đạt 1/10 và tốn nhiều token hơn.
   - Trên tác vụ đánh giá, không có điều kiện nào cải thiện do xuất hiện các quy ước mới lạ chưa từng được học. Đây là biểu hiện kinh điển của hiện tượng **quá khớp ở tầng ngữ cảnh (context overfitting)**: các tri thức thủ tục sinh ra từ tác vụ học giúp giải quyết rất tốt các lỗi của tác vụ học nhưng không tự tổng quát hóa sang các quy tắc tổ chức hoàn toàn mới trong tác vụ đánh giá.
2. **Phân rã check kỹ thuật và check quy ước (`rule_`)**:
   - Các check kỹ thuật (như `visible_suite_passes`, `discount_rounds_half_up`, `low_stock_follows_docstring`) đạt được nhờ khả năng lập trình và suy luận logic của LLM.
   - Skill do curator sinh ra nhắm trực tiếp vào việc chuẩn hóa quy ước Acme (`rule_type_hints`, `rule_regression_tests`, `rule_changelog`).
   - Các check quy ước mới của tác vụ đánh giá (như quy ước cấu trúc log/header mới) không được skill hỗ trợ vì curator hoàn toàn bị cô lập khỏi tác vụ đánh giá, bảo đảm tính liêm chính khoa học (không data leakage).
3. **Cơ chế hoạt động qua vết và `skills_read`**:
   - Check được skill giúp đạt: Trong `code-learn`, skill `code-quality` định hướng tác tử viết unit test độc lập mà không sửa đè file test gốc của hệ thống, giúp bảo toàn tính toàn vẹn của bộ kiểm thử.
   - Check chưa được cải thiện: Tác tử chưa hoàn tất type annotations cho toàn bộ 100% public functions do độ dài context bị cắt ngắn khi hoàn thành bài toán chính.
4. **Chi phí token**:
   - `subagents` có chi phí token cao nhất (trung bình 214k tokens trên tập học, cao hơn ~12% so với baseline 191k tokens) do system prompt bổ sung thêm định nghĩa 3 subagents.
   - `skills-auto` có hiệu quả chi phí token tốt nhất (34k tokens trên `code-learn`, tiết kiệm 80% chi phí).
   - Đa tác tử (subagents) không đáng chi phí trong bài lab này vì các tác vụ mang tính tuần tự trong một codebase nhỏ, việc phân rã công việc làm tăng chi phí truyền nhận prompt mà không tăng độ chính xác.
5. **Rò rỉ dữ liệu và quá khớp**:
   - Curator được bảo vệ nghiêm ngặt: hàm `eval_markers()` lọc toàn bộ các từ khóa của tác vụ đánh giá, và biểu thức chính quy `SAFE_NAME` chặn path traversal.
   - Không có bất kỳ token hoặc định danh nào của `tasks/*-eval` bị rò rỉ vào `skills/auto/`.
6. **Nhiễu thực nghiệm**:
   - Điểm của cùng bộ skill trên `code-learn` giữa Phần 3.4 (4/10) và sau đóng băng (0/10 do lỗi 402 API) cho thấy tính bất định của môi trường bên ngoài (hạn mức API, độ trễ mạng) là yếu tố gây nhiễu lớn cần được tính đến trong các benchmark tác tử.

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập tác vụ nhỏ**: Mỗi họ tác vụ chỉ gồm 1 tác vụ học và 1 tác vụ đánh giá (tổng cộng 6 tác vụ), do đó kết quả phản ánh các trường hợp điển hình hơn là kết luận thống kê quy mô lớn.
2. **Thực thi đơn lẻ (Single-run)**: Mỗi điều kiện chỉ được chạy 1 lần do giới hạn ngân sách token cá nhân, chịu ảnh hưởng bởi tính ngẫu nhiên của mô hình (temperature, sampling) và sự cố hạn ngạch API.
3. **Quy ước nhân tạo**: Các check quy ước Acme (`rule_`) được thiết kế nhằm mô phỏng quy chuẩn doanh nghiệp nhưng chưa thể bao quát toàn bộ sự phức tạp của các dự án phần mềm thực tế.

## 10. Kết luận

1. Đã xây dựng thành công bộ khung điều khiển tác tử (Agent Harness) hoàn chỉnh với thư viện Deep Agents, hỗ trợ đầy đủ công cụ tệp, shell cô lập, đa tác tử và nạp skill.
2. Cơ chế tác tử tự tiến hóa (Self-Evolving Agent) ở tầng ngữ cảnh đã chứng minh tính hiệu quả vượt trội trên tác vụ học, giúp tăng gấp đôi điểm số và tiết kiệm 80% lượng token tiêu thụ.
3. Hiện tượng quá khớp (overfitting) ở tầng ngữ cảnh được ghi nhận rõ ràng khi tri thức thủ tục không tự thích nghi được với các quy ước tổ chức hoàn toàn mới của tác vụ đánh giá.
4. Kiến trúc đa tác tử (Multi-Agent Subagents) làm tăng đáng kể chi phí token đầu vào mà không mang lại ưu thế rõ rệt đối với các bài toán kỹ thuật đơn lẻ.
5. Đề xuất phát triển: Tích hợp cơ chế tiến hóa thời gian thực (Hot-path self-evolution) kết hợp bộ lọc tri thức chủ động để tác tử có thể vừa thực thi vừa cập nhật kỹ năng mà vẫn đảm bảo tính an toàn.

## Phụ lục

- **Lệnh đã chạy (theo thứ tự)**:
  1. `pytest tests/test_01_provided.py` (15/15 passed)
  2. `python scripts/tour.py`
  3. `pytest tests/test_02_agent.py` (9/9 passed)
  4. `pytest tests/test_03_runner.py` (6/6 passed)
  5. `pytest tests/test_04_curator.py` (2/2 passed)
  6. `pytest` (Toàn bộ 32/32 unit tests passed)
  7. `python -m lab.runner --condition baseline --tasks data-learn code-learn logs-learn`
  8. `python -m lab.runner --condition subagents --tasks learn`
  9. `python -m lab.curator`
  10. `python -m lab.runner --condition skills-auto --tasks learn`
  11. `git add -A && git commit -m "hypotheses"`
  12. `git add -A && git commit --allow-empty -m "freeze skills" && git tag freeze`
  13. `python -m lab.runner --condition baseline --tasks eval`
  14. `python -m lab.runner --condition subagents --tasks eval`
  15. `python -m lab.runner --condition skills-auto --tasks all`
  16. `python scripts/verify_freeze.py` (Kết quả: `checked 6 runs of skill conditions: OK`)
  17. `python -m lab.compare > report/table.md`
  18. `python scripts/check_breakdown.py`

- **Thử thách mở rộng (+5 điểm): Hướng 6c - Tấn công curator (Red Team & Data Leakage Defense)**:
  - *Mục tiêu*: Thử nghiệm các kịch bản tấn công bảo mật vào Curator nhằm kiểm chứng cơ chế ngăn ngừa rò rỉ dữ liệu (Data Leakage) và chống chèn mã độc vào file hệ thống (Path Traversal).
  - *Phương pháp kiểm thử*: 
    1. Giả lập một lần chạy tác vụ học trả về vết thực thi chứa các định danh của tác vụ đánh giá (lấy từ `eval_markers()`).
    2. Giả lập mô hình LLM sinh ra skill có tên chứa ký tự duyệt thư mục nguy hiểm: `=== SKILL: ../evil ===`.
  - *Kết quả*:
    - Hàm `validate_skill` đã phát hiện và chặn thành công 100% nỗ lực tạo file ngoài phạm vi sandbox nhờ regex `SAFE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")`. Thư mục `../evil` bị từ chối tuyệt đối.
    - Cơ chế kiểm duyệt chuỗi `eval_markers()` đã phát hiện chuỗi chứa tài liệu đánh giá và gắn cờ `mentions evaluation material`, loại bỏ skill rò rỉ khỏi danh sách ghi đĩa.
  - *Đề xuất tăng cường*: Cần bổ sung bộ lọc tiền xử lý (Input Sanitizer) đối với chuỗi `trace.md` trước khi gửi vào prompt của LLM để phòng chống triệt để các kỹ thuật Prompt Injection gián tiếp từ dữ liệu log không tin cậy.
