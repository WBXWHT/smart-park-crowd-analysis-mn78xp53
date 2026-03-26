import json
import random
import datetime
from typing import Dict, List, Tuple

class CrowdAnalyzer:
    """人流密度分析模拟类"""
    
    def __init__(self):
        self.cameras = ["北门入口", "南门出口", "中央广场", "办公楼入口", "餐厅区域"]
        
    def get_crowd_density(self) -> Dict[str, float]:
        """模拟获取各摄像头人流密度（0-1之间）"""
        density = {}
        for camera in self.cameras:
            # 模拟不同区域的人流密度
            if "入口" in camera:
                base = 0.6 + random.uniform(-0.2, 0.3)
            elif "广场" in camera:
                base = 0.4 + random.uniform(-0.2, 0.3)
            else:
                base = 0.3 + random.uniform(-0.2, 0.2)
            
            density[camera] = max(0.1, min(0.95, base))  # 限制在0.1-0.95之间
        
        return density
    
    def predict_peak_hours(self, density_data: Dict[str, float]) -> List[str]:
        """基于当前密度预测高峰时段"""
        avg_density = sum(density_data.values()) / len(density_data)
        
        current_hour = datetime.datetime.now().hour
        peak_hours = []
        
        # 根据当前密度预测未来高峰
        if avg_density > 0.7:
            peak_hours = [f"{current_hour+1}:00", f"{current_hour+2}:00"]
        elif avg_density > 0.5:
            peak_hours = [f"{current_hour+1}:00"]
        else:
            peak_hours = ["无明显高峰"]
            
        return peak_hours

class WorkOrderAnalyzer:
    """工单文本分析模拟类"""
    
    def __init__(self):
        self.keywords = {
            "crowd": ["拥挤", "人多", "排队", "拥堵", "密集"],
            "facility": ["故障", "损坏", "维修", "无法使用", "坏了"],
            "security": ["安全", "纠纷", "冲突", "报警", "紧急"]
        }
    
    def analyze_text(self, work_order_text: str) -> Dict[str, any]:
        """分析工单文本，提取关键信息"""
        analysis_result = {
            "urgency_level": "低",
            "main_issue": "其他",
            "keywords_found": [],
            "suggested_action": "常规处理"
        }
        
        # 检查文本中的关键词
        found_keywords = []
        for category, words in self.keywords.items():
            for word in words:
                if word in work_order_text:
                    found_keywords.append(word)
                    if category == "crowd":
                        analysis_result["main_issue"] = "人流管理"
                        analysis_result["urgency_level"] = "高"
                        analysis_result["suggested_action"] = "立即调度人员疏导"
                    elif category == "security":
                        analysis_result["main_issue"] = "安保事件"
                        analysis_result["urgency_level"] = "高"
                        analysis_result["suggested_action"] = "通知安保部门"
        
        analysis_result["keywords_found"] = found_keywords
        
        # 如果没有找到关键词但文本较长，设为中等紧急
        if not found_keywords and len(work_order_text) > 20:
            analysis_result["urgency_level"] = "中"
            analysis_result["suggested_action"] = "24小时内处理"
        
        return analysis_result

class SmartParkAnalysisPlatform:
    """智慧园区分析平台主类"""
    
    def __init__(self):
        self.crowd_analyzer = CrowdAnalyzer()
        self.workorder_analyzer = WorkOrderAnalyzer()
        
    def generate_daily_report(self) -> Dict[str, any]:
        """生成每日分析报告"""
        # 获取人流数据
        crowd_data = self.crowd_analyzer.get_crowd_density()
        peak_hours = self.crowd_analyzer.predict_peak_hours(crowd_data)
        
        # 模拟工单数据
        sample_work_orders = [
            "北门入口排队人数过多，需要增加引导人员",
            "中央广场的喷泉设备故障，需要维修",
            "餐厅区域发生轻微纠纷，已现场调解"
        ]
        
        # 分析工单
        workorder_analysis = []
        for order in sample_work_orders:
            analysis = self.workorder_analyzer.analyze_text(order)
            workorder_analysis.append({
                "work_order": order,
                "analysis": analysis
            })
        
        # 计算调度效率提升（模拟）
        avg_density = sum(crowd_data.values()) / len(crowd_data)
        efficiency_improvement = round(avg_density * 25, 1)  # 模拟计算效率提升
        
        # 生成报告
        report = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "crowd_density": crowd_data,
            "peak_hour_prediction": peak_hours,
            "workorder_analysis": workorder_analysis,
            "efficiency_improvement": f"{efficiency_improvement}%",
            "recommendations": self._generate_recommendations(crowd_data, workorder_analysis)
        }
        
        return report
    
    def _generate_recommendations(self, crowd_data: Dict[str, float], 
                                 workorder_analysis: List[Dict]) -> List[str]:
        """生成调度建议"""
        recommendations = []
        
        # 基于人流密度的建议
        for location, density in crowd_data.items():
            if density > 0.7:
                recommendations.append(f"{location}人流密集，建议增派疏导人员")
            elif density > 0.5:
                recommendations.append(f"{location}人流中等，保持当前调度")
        
        # 基于工单分析的建议
        for analysis in workorder_analysis:
            if analysis["analysis"]["urgency_level"] == "高":
                recommendations.append(f"紧急工单：{analysis['work_order'][:20]}...")
        
        if not recommendations:
            recommendations.append("当前园区运行平稳，保持常规调度")
        
        return recommendations[:3]  # 返回最重要的3条建议
    
    def print_report(self, report: Dict[str, any]):
        """打印分析报告"""
        print("=" * 60)
        print("智慧园区人流分析平台 - 实时报告")
        print("=" * 60)
        print(f"生成时间: {report['timestamp']}")
        print(f"\n📊 人流密度分析:")
        for location, density in report["crowd_density"].items():
            level = "高" if density > 0.7 else "中" if density > 0.5 else "低"
            print(f"  {location}: {density:.2f} ({level})")
        
        print(f"\n⏰ 高峰时段预测: {', '.join(report['peak_hour_prediction'])}")
        
        print(f"\n📝 工单文本分析:")
        for i, item in enumerate(report["workorder_analysis"], 1):
            analysis = item["analysis"]
            print(f"  工单{i}: {item['work_order']}")
            print(f"    主要问题: {analysis['main_issue']}")
            print(f"    紧急程度: {analysis['urgency_level']}")
        
        print(f"\n🚀 调度效率提升: {report['efficiency_improvement']}")
        
        print(f"\n💡 调度建议:")
        for i, rec in enumerate(report["recommendations"], 1):
            print(f"  {i}. {rec}")
        
        print("=" * 60)

def main():
    """主函数"""
    print("正在启动智慧园区人流分析平台...")
    print("模拟AI视觉分析（人流密度识别）与语义AI（工单文本分析）...\n")
    
    # 创建平台实例
    platform = SmartParkAnalysisPlatform()
    
    # 生成并显示报告
    report = platform.generate_daily_report()
    platform.print_report(report)
    
    # 模拟API调用（注释掉实际请求）
    # response = requests.post("https://api.smartpark.com/analysis", json=report)
    # print(f"报告已上传，状态码: {response.status_code}")
    
    print("\n✅ 分析完成！客户可通过该功能提升高峰时段调度效率。")

if __name__ == "__main__":
    main()