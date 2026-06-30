import csv
import json

data = []
with open(r'D:\桌面2.0\数据分析\house_data\house_data_cleaned_for_tableau.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append({
            'district': row['district'],
            'total_price': float(row['total_price']),
            'unit_price': float(row['unit_price']),
            'total_area': float(row['total_area']),
            'house_age': int(float(row['house_age'])),
            'area_range': row['area_range'],
            'age_range': row['age_range'],
            'decoration': row['装修情况'],
            'floor': row['楼层'],
            'community': row['小区名称']
        })

html_template = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>长沙二手房数据可视化仪表盘</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #fff;
        }
        .header {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding: 20px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .header h1 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .header .subtitle {
            color: #8892b0;
            font-size: 14px;
            margin-top: 4px;
        }
        .header .badge {
            background: linear-gradient(135deg, #00d4ff, #7b2cbf);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        .kpi-section {
            padding: 30px 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .kpi-card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .kpi-value.blue { color: #00d4ff; }
        .kpi-value.purple { color: #a855f7; }
        .kpi-value.green { color: #00ff88; }
        .kpi-value.orange { color: #ffaa00; }
        .kpi-label {
            color: #8892b0;
            font-size: 14px;
        }
        .charts-section {
            padding: 20px 40px 40px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        .chart-container {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .chart-title {
            font-size: 18px;
            font-weight: 600;
            color: #e6f1ff;
            margin-bottom: 20px;
        }
        .chart-body {
            height: 300px;
        }
        .chart-body.large {
            height: 400px;
        }
        .full-width {
            grid-column: 1 / -1;
        }
        .filter-bar {
            padding: 0 40px 20px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        .filter-group {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .filter-label {
            color: #8892b0;
            font-size: 14px;
        }
        .filter-select {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.1);
            color: #fff;
            padding: 8px 15px;
            border-radius: 10px;
            font-size: 13px;
            cursor: pointer;
            outline: none;
        }
        .filter-select option {
            background: #16213e;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        .data-table th, .data-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 13px;
        }
        .data-table th {
            color: #8892b0;
            font-weight: 500;
        }
        .data-table td {
            color: #ccd6f6;
        }
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #1a1a2e;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(0,212,255,0.2);
            border-top-color: #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="loading-overlay" id="loading">
        <div class="loading-spinner"></div>
    </div>
    <header class="header">
        <div>
            <h1>🏠 长沙二手房数据可视化仪表盘</h1>
            <div class="subtitle">基于真实房源数据分析 | 实时筛选</div>
        </div>
        <div class="badge">📊 数据更新: 2025年</div>
    </header>
    <section class="kpi-section">
        <div class="kpi-card">
            <div class="kpi-value blue" id="kpi-count">0</div>
            <div class="kpi-label">房源总数</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value purple" id="kpi-avg-price">0</div>
            <div class="kpi-label">平均总价 (万)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value green" id="kpi-unit-price">0</div>
            <div class="kpi-label">平均单价 (元/㎡)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value orange" id="kpi-area">0</div>
            <div class="kpi-label">平均面积 (㎡)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-value blue" id="kpi-age">0</div>
            <div class="kpi-label">平均房龄 (年)</div>
        </div>
    </section>
    <div class="filter-bar">
        <div class="filter-group">
            <span class="filter-label">区域筛选:</span>
            <select class="filter-select" id="districtFilter" onchange="updateCharts()">
                <option value="all">全部区域</option>
                <option value="岳麓">岳麓区</option>
                <option value="雨花">雨花区</option>
                <option value="天心">天心区</option>
                <option value="开福">开福区</option>
                <option value="芙蓉">芙蓉区</option>
                <option value="望城">望城区</option>
                <option value="长沙县">长沙县</option>
                <option value="宁乡">宁乡市</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">面积段:</span>
            <select class="filter-select" id="areaFilter" onchange="updateCharts()">
                <option value="all">全部</option>
                <option value="小户型(<90㎡)">小户型 (<90㎡)</option>
                <option value="中户型(90-144㎡)">中户型 (90-144㎡)</option>
                <option value="大户型(>144㎡)">大户型 (>144㎡)</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">装修:</span>
            <select class="filter-select" id="decoFilter" onchange="updateCharts()">
                <option value="all">全部</option>
                <option value="精装">精装修</option>
                <option value="毛坯">毛坯</option>
                <option value="简装">简装</option>
                <option value="其他">其他</option>
            </select>
        </div>
    </div>
    <section class="charts-section">
        <div class="chart-container">
            <div class="chart-title">各区域平均单价对比</div>
            <div class="chart-body" id="chart1"></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">房源总价分布</div>
            <div class="chart-body" id="chart2"></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">面积段分布</div>
            <div class="chart-body" id="chart3"></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">房龄段分布</div>
            <div class="chart-body" id="chart4"></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">装修情况分布</div>
            <div class="chart-body" id="chart5"></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">楼层分布</div>
            <div class="chart-body" id="chart7"></div>
        </div>
        <div class="chart-container full-width">
            <div class="chart-title">面积-单价关系分析</div>
            <div class="chart-body large" id="chart6"></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">各区域房源数量</div>
            <div class="chart-body" id="chart8"></div>
        </div>
        <div class="chart-container full-width">
            <div class="chart-title">区域详细数据</div>
            <table class="data-table" id="dataTable">
                <thead>
                    <tr>
                        <th>区域</th>
                        <th>房源数</th>
                        <th>平均总价(万)</th>
                        <th>中位总价(万)</th>
                        <th>平均单价(元/㎡)</th>
                        <th>平均面积(㎡)</th>
                    </tr>
                </thead>
                <tbody id="tableBody"></tbody>
            </table>
        </div>
    </section>
    <script>
        const rawData = %DATA%;
        let charts = {};

        function filterData() {
            const district = document.getElementById('districtFilter').value;
            const areaRange = document.getElementById('areaFilter').value;
            const deco = document.getElementById('decoFilter').value;
            
            return rawData.filter(item => {
                if (district !== 'all' && item.district !== district) return false;
                if (areaRange !== 'all' && item.area_range !== areaRange) return false;
                if (deco !== 'all' && item.decoration !== deco) return false;
                return true;
            });
        }

        function calculateStats(data) {
            if (data.length === 0) return null;
            
            const totalPrices = data.map(d => d.total_price);
            const unitPrices = data.map(d => d.unit_price);
            const areas = data.map(d => d.total_area);
            const ages = data.map(d => d.house_age);
            
            return {
                count: data.length,
                avgPrice: totalPrices.reduce((a, b) => a + b, 0) / data.length,
                medianPrice: totalPrices.sort((a, b) => a - b)[Math.floor(data.length / 2)],
                avgUnitPrice: unitPrices.reduce((a, b) => a + b, 0) / data.length,
                avgArea: areas.reduce((a, b) => a + b, 0) / data.length,
                avgAge: ages.reduce((a, b) => a + b, 0) / data.length
            };
        }

        function updateKPIs(stats) {
            document.getElementById('kpi-count').textContent = stats.count;
            document.getElementById('kpi-avg-price').textContent = stats.avgPrice.toFixed(1);
            document.getElementById('kpi-unit-price').textContent = Math.round(stats.avgUnitPrice);
            document.getElementById('kpi-area').textContent = stats.avgArea.toFixed(1);
            document.getElementById('kpi-age').textContent = stats.avgAge.toFixed(1);
        }

        function initCharts() {
            charts.chart1 = echarts.init(document.getElementById('chart1'));
            charts.chart2 = echarts.init(document.getElementById('chart2'));
            charts.chart3 = echarts.init(document.getElementById('chart3'));
            charts.chart4 = echarts.init(document.getElementById('chart4'));
            charts.chart5 = echarts.init(document.getElementById('chart5'));
            charts.chart6 = echarts.init(document.getElementById('chart6'));
            charts.chart7 = echarts.init(document.getElementById('chart7'));
            charts.chart8 = echarts.init(document.getElementById('chart8'));
            updateCharts();
        }

        function updateCharts() {
            const data = filterData();
            const stats = calculateStats(data);
            
            if (!stats) {
                alert('没有符合条件的数据！');
                return;
            }
            
            updateKPIs(stats);
            
            const districtStats = {};
            data.forEach(d => {
                if (!districtStats[d.district]) {
                    districtStats[d.district] = { count: 0, totalPrice: 0, unitPrice: 0, area: 0, prices: [] };
                }
                districtStats[d.district].count++;
                districtStats[d.district].totalPrice += d.total_price;
                districtStats[d.district].unitPrice += d.unit_price;
                districtStats[d.district].area += d.total_area;
                districtStats[d.district].prices.push(d.total_price);
            });
            
            const districtNames = Object.keys(districtStats).sort();
            const districtUnitPrices = districtNames.map(d => districtStats[d].unitPrice / districtStats[d].count);
            
            charts.chart1.setOption({
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                xAxis: { type: 'category', data: districtNames, axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' } },
                yAxis: { type: 'value', axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    data: districtUnitPrices,
                    type: 'bar',
                    barWidth: '50%',
                    itemStyle: {
                        borderRadius: [8, 8, 0, 0],
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#00d4ff' },
                            { offset: 1, color: '#7b2cbf' }
                        ])
                    },
                    label: { show: true, position: 'top', color: '#00d4ff', formatter: '{c0}' }
                }]
            });
            
            const priceBins = [0, 50, 80, 100, 150, 200, 300, 500];
            const priceLabels = ['<50万', '50-80万', '80-100万', '100-150万', '150-200万', '200-300万', '>300万'];
            const priceCounts = priceLabels.map(() => 0);
            data.forEach(d => {
                for (let i = 0; i < priceBins.length - 1; i++) {
                    if (d.total_price >= priceBins[i] && d.total_price < priceBins[i + 1]) {
                        priceCounts[i]++;
                        break;
                    }
                }
                if (d.total_price >= 300) priceCounts[6]++;
            });
            
            charts.chart2.setOption({
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                xAxis: { type: 'category', data: priceLabels, axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' } },
                yAxis: { type: 'value', axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    data: priceCounts,
                    type: 'bar',
                    barWidth: '60%',
                    itemStyle: {
                        borderRadius: [8, 8, 0, 0],
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#a855f7' },
                            { offset: 1, color: '#ec4899' }
                        ])
                    },
                    label: { show: true, position: 'top', color: '#a855f7' }
                }]
            });
            
            const areaRangeCounts = {};
            data.forEach(d => {
                areaRangeCounts[d.area_range] = (areaRangeCounts[d.area_range] || 0) + 1;
            });
            
            charts.chart3.setOption({
                tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
                legend: { orient: 'vertical', right: '5%', top: 'center', textStyle: { color: '#8892b0' } },
                series: [{
                    type: 'pie',
                    radius: ['40%', '70%'],
                    center: ['40%', '50%'],
                    itemStyle: { borderRadius: 10, borderColor: '#1a1a2e', borderWidth: 2 },
                    label: { show: false },
                    emphasis: { label: { show: true, fontSize: 20, fontWeight: 'bold', color: '#fff' } },
                    data: Object.entries(areaRangeCounts).map(([name, value]) => ({
                        name, value,
                        itemStyle: { color: name.includes('小') ? '#00d4ff' : name.includes('中') ? '#7b2cbf' : '#ff6b6b' }
                    }))
                }]
            });
            
            const ageRangeCounts = {};
            data.forEach(d => {
                ageRangeCounts[d.age_range] = (ageRangeCounts[d.age_range] || 0) + 1;
            });
            const ageOrder = ['新房(0-5年)', '次新房(6-10年)', '老房(11-20年)', '老旧房(>20年)'];
            const ageNames = ageOrder.filter(n => ageRangeCounts[n]);
            const ageValues = ageNames.map(n => ageRangeCounts[n]);
            
            charts.chart4.setOption({
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                xAxis: { type: 'category', data: ageNames, axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' } },
                yAxis: { type: 'value', axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    data: ageValues,
                    type: 'bar',
                    barWidth: '50%',
                    itemStyle: {
                        borderRadius: [8, 8, 0, 0],
                        color: function(params) {
                            const colors = ['#00ff88', '#00d4ff', '#7b2cbf', '#ff6b6b'];
                            return colors[params.dataIndex % 4];
                        }
                    },
                    label: { show: true, position: 'top', color: '#fff' }
                }]
            });
            
            const decoCounts = {};
            data.forEach(d => {
                decoCounts[d.decoration] = (decoCounts[d.decoration] || 0) + 1;
            });
            
            charts.chart5.setOption({
                tooltip: { trigger: 'item' },
                series: [{
                    type: 'pie',
                    radius: '70%',
                    center: ['50%', '50%'],
                    roseType: 'area',
                    itemStyle: { borderRadius: 8 },
                    label: { color: '#8892b0' },
                    data: Object.entries(decoCounts).map(([name, value], index) => ({
                        name, value,
                        itemStyle: { color: ['#00d4ff', '#a855f7', '#00ff88', '#ffaa00'][index % 4] }
                    }))
                }]
            });
            
            const scatterData = data.map(d => [d.total_area, d.unit_price, d.total_price, d.house_age]);
            charts.chart6.setOption({
                tooltip: {
                    formatter: function(params) {
                        return `面积: ${params.data[0].toFixed(1)}㎡<br/>单价: ${params.data[1].toFixed(0)}元/㎡<br/>总价: ${params.data[2]}万<br/>房龄: ${params.data[3]}年`;
                    }
                },
                grid: { left: '5%', right: '8%', bottom: '10%', top: '10%' },
                xAxis: { type: 'value', name: '面积 (㎡)', nameTextStyle: { color: '#8892b0' },
                yAxis: { type: 'value', name: '单价 (元/㎡)', nameTextStyle: { color: '#8892b0' },
                visualMap: { min: 0, max: 25, dimension: 3, orient: 'vertical', right: '2%', top: 'center', text: ['新房', '老房'], textStyle: { color: '#8892b0' }, calculable: true, inRange: { color: ['#00ff88', '#00d4ff', '#7b2cbf', '#ff6b6b'] } },
                series: [{
                    type: 'scatter',
                    data: scatterData,
                    symbolSize: function(data) { return Math.sqrt(data[2]) * 2 + 5; },
                    itemStyle: { opacity: 0.6 }
                }]
            });
            
            const floorCounts = {};
            data.forEach(d => {
                floorCounts[d.floor] = (floorCounts[d.floor] || 0) + 1;
            });
            
            charts.chart7.setOption({
                tooltip: { trigger: 'item' },
                series: [{
                    type: 'pie',
                    radius: ['30%', '65%'],
                    center: ['50%', '50%'],
                    itemStyle: { borderRadius: 10, borderColor: '#1a1a2e', borderWidth: 2 },
                    label: { show: true, formatter: '{b}\\\\n{c}套 ({d}%)', color: '#8892b0' },
                    data: Object.entries(floorCounts).map(([name, value], index) => ({
                        name, value,
                        itemStyle: { color: ['#74b9ff', '#55efc4', '#ff7675'][index % 3] }
                    }))
                }]
            });
            
            const districtCounts = districtNames.map(d => districtStats[d].count);
            charts.chart8.setOption({
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
                xAxis: { type: 'category', data: districtNames, axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0', rotate: 30 } },
                yAxis: { type: 'value', axisLine: { lineStyle: { color: '#8892b0' }, axisLabel: { color: '#8892b0' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } } },
                series: [{
                    data: districtCounts,
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 10,
                    lineStyle: { width: 3, color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                        { offset: 0, color: '#00d4ff' },
                        { offset: 1, color: '#7b2cbf' }
                    ]) },
                    areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(0,212,255,0.3)' },
                        { offset: 1, color: 'rgba(123,44,191,0.05)' }
                    ]) },
                    itemStyle: { color: '#00d4ff', borderColor: '#fff', borderWidth: 2 }
                }]
            });
            
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            districtNames.forEach(name => {
                const d = districtStats[name];
                const row = document.createElement('tr');
                const sortedPrices = d.prices.sort((a, b) => a - b);
                const medianPrice = sortedPrices[Math.floor(sortedPrices.length / 2)];
                row.innerHTML = `
                    <td><strong>${name}</strong></td>
                    <td>${d.count}</td>
                    <td>${(d.totalPrice / d.count).toFixed(1)}</td>
                    <td>${medianPrice.toFixed(1)}</td>
                    <td>${Math.round(d.unitPrice / d.count)}</td>
                    <td>${(d.area / d.count).toFixed(1)}</td>
                `;
                tbody.appendChild(row);
            });
        }

        window.addEventListener('resize', () => {
            Object.values(charts).forEach(chart => chart.resize());
        });

        window.addEventListener('load', () => {
            setTimeout(() => {
                document.getElementById('loading').style.opacity = '0';
                setTimeout(() => {
                    document.getElementById('loading').style.display = 'none';
                }, 500);
                initCharts();
            }, 500);
        });
    </script>
</body>
</html>
'''

html_content = html_template.replace('%DATA%', json.dumps(data))

with open(r'D:\桌面2.0\数据分析\house_data\house_python.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML 文件已生成！")
