# 文化活动消费观察

文化活动、票券和商户交易。当前总览只按商户汇总交易金额。

样例数据均为本地合成记录，不对应真实个人、媒体、机构或交易。项目使用 Python 3.11.2 标准库，数据随项目保存，不访问外部服务。

## 使用

在项目根目录运行 `python3 -m app summary` 查看按当前基础口径生成的 JSON 总览。

## 验证

运行 `python3 -m unittest discover -s tests -v` 和 `python3 -m compileall -q app tests`。

## 结构

`data/data.json` 保存领域记录与基础汇总口径；`app/storage.py` 读取并检查数据形状；`app/analysis.py` 计算基础分组统计；`app/service.py` 组合数据读取和统计；`tests/` 验证产品入口及无效数据处理。

## 工作台

场地当前按活动净销售额结算。`calendar` 查看实际举办状态，`turnover` 看原单与全量退款合并后的分单净额，`settle` 保存当前场地结算单，`receipts` 读回已保存的结算单。金额统一使用分；场地方费用向下取整到分。活动取消不出结算单。结算归档后不可覆盖。

例如在项目根目录运行 `python3 -m app turnover --key harbor-fair`。`day_status` 记录每日商户是否营业及报数是否完整，`controls` 是运营选的参考日期；`passes` 记录联票可用商户和容量，销售的 `pass` 为空表示未出示联票。现行结算只按收银归属的 `event` 认单，不使用这两类资料。

操作数据在 `data/workbench.json`。工作台涉及的领域代码：`calendar` 检查活动是否可结算, `tills` 对账和识别退款, `settlement` 决定场地的结算金额。已有总览仍使用 `data/data.json`。
