import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ScatterChart, Scatter, ReferenceLine
} from 'recharts';
import { 
  BookOpen, Users, Zap, Shield, TrendingUp, 
  Activity, MousePointer2, FileText, Share2, Target, GitCommit,
  Network, BarChart2, Globe, Search, Lightbulb, ChevronDown, Menu, X, ArrowRight
} from 'lucide-react';

// --- 1. 数据部分 (Data) ---

// 1.1 样本分布
const demographicsData = [
  { name: '男性', value: 62.7, fill: '#3b82f6' },
  { name: '女性', value: 37.3, fill: '#ec4899' },
];

// 1.2 学历差异 (Dumbbell Data)
const dumbbellData = [
  { category: '政策支持', undergraduate: 4.15, master: 4.17, phd: 4.41 },
  { category: '技术信任', undergraduate: 4.00, master: 4.22, phd: 4.41 },
  { category: '责任感', undergraduate: 3.56, master: 3.90, phd: 3.92 },
  { category: '知识水平', undergraduate: 3.81, master: 3.98, phd: 3.99 },
];

// 1.3 雷达图数据 (性别对比)
const genderRadarData = [
  { subject: '技术信任', A: 4.04, B: 4.36, fullMark: 5 },
  { subject: 'EV技术认知', A: 3.86, B: 4.13, fullMark: 5 },
  { subject: '政策执行', A: 4.21, B: 4.14, fullMark: 5 },
  { subject: '政策支持度', A: 4.50, B: 4.43, fullMark: 5 },
  { subject: '限油支持', A: 4.18, B: 3.91, fullMark: 5 },
];

// 1.4 风险数据 (条形图)
const riskData = [
  { name: '高昂价格', impact: -0.26, worry: 47 },
  { name: '里程焦虑', impact: -0.21, worry: 59 },
  { name: '充电不便', impact: -0.40, worry: 67 },
  { name: '电池安全', impact: 0.28, worry: 72 },
  { name: '整体安全', impact: 0.01, worry: 72 },
];

// 1.5 PCA 散点图模拟数据
const pcaData = [
  { x: 2.5, y: 1.1, type: '高意愿 (High Int)', fill: '#f87171' }, 
  { x: 1.8, y: 0.8, type: '高意愿 (High Int)', fill: '#f87171' },
  { x: 2.1, y: -0.5, type: '高意愿 (High Int)', fill: '#f87171' },
  { x: 1.2, y: -2.0, type: '高意愿 (High Int)', fill: '#f87171' },
  { x: 0.5, y: -1.5, type: '高意愿 (High Int)', fill: '#f87171' },
  { x: 0.2, y: 0.8, type: '中意愿 (Med Int)', fill: '#fbbf24' },
  { x: -0.5, y: 0.5, type: '中意愿 (Med Int)', fill: '#fbbf24' },
  { x: -1.2, y: 1.2, type: '中意愿 (Med Int)', fill: '#fbbf24' },
  { x: -1.5, y: -0.8, type: '低意愿 (Low Int)', fill: '#94a3b8' },
  { x: -2.0, y: 0.2, type: '低意愿 (Low Int)', fill: '#94a3b8' },
  { x: -0.8, y: -2.2, type: '低意愿 (Low Int)', fill: '#94a3b8' },
  { x: -2.5, y: -0.3, type: '低意愿 (Low Int)', fill: '#94a3b8' },
];

// 1.6 相关性弦图数据模拟
const chordNodes = [
  { id: 'Trust', label: '信任', color: '#f87171', angle: 0 },
  { id: 'Policy', label: '政策', color: '#818cf8', angle: 60 },
  { id: 'Attitude', label: '态度', color: '#64748b', angle: 120 },
  { id: 'Intention', label: '意愿', color: '#34d399', angle: 180 },
  { id: 'Know', label: '认知', color: '#a78bfa', angle: 240 },
  { id: 'Resp', label: '责任', color: '#fbbf24', angle: 300 },
];

const chordLinks = [
  { source: 'Policy', target: 'Trust', value: 0.54, width: 6 },
  { source: 'Trust', target: 'Attitude', value: 0.52, width: 5 },
  { source: 'Trust', target: 'Intention', value: 0.45, width: 4 },
  { source: 'Attitude', target: 'Intention', value: 0.45, width: 4 },
  { source: 'Policy', target: 'Intention', value: 0.49, width: 5 },
  { source: 'Know', target: 'Trust', value: 0.22, width: 2 },
  { source: 'Resp', target: 'Attitude', value: 0.27, width: 3 },
];

// --- 组件部分 (Components) ---

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollTo = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsOpen(false);
    }
  };

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/90 backdrop-blur-md shadow-sm py-3' : 'bg-transparent py-5'}`}>
      <div className="max-w-6xl mx-auto px-6 flex justify-between items-center">
        <div className={`font-bold text-xl flex items-center space-x-2 ${scrolled ? 'text-slate-800' : 'text-white'}`}>
          <Zap size={24} className="text-emerald-500" />
          <span>EV Research 2024</span>
        </div>
        
        {/* Desktop Menu */}
        <div className={`hidden md:flex space-x-8 font-medium ${scrolled ? 'text-slate-600' : 'text-slate-200'}`}>
          {['背景', '方法', '数据探索', '结论'].map((item, idx) => {
             const ids = ['background', 'methodology', 'dashboard', 'conclusion'];
             return (
               <button 
                 key={item} 
                 onClick={() => scrollTo(ids[idx])}
                 className="hover:text-emerald-500 transition-colors"
               >
                 {item}
               </button>
             )
          })}
        </div>

        {/* Mobile Menu Button */}
        <button className="md:hidden text-emerald-500" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 bg-white shadow-lg border-t border-slate-100 p-4 flex flex-col space-y-4 md:hidden">
          {['背景', '方法', '数据探索', '结论'].map((item, idx) => {
             const ids = ['background', 'methodology', 'dashboard', 'conclusion'];
             return (
               <button 
                 key={item} 
                 onClick={() => scrollTo(ids[idx])}
                 className="text-left text-slate-600 font-medium py-2"
               >
                 {item}
               </button>
             )
          })}
        </div>
      )}
    </nav>
  );
};

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-xl shadow-sm border border-slate-100 p-6 transition-all hover:shadow-md ${className}`}>
    {children}
  </div>
);

const SectionTitle = ({ title, subtitle, light = false }) => (
  <div className="mb-12 text-center max-w-3xl mx-auto">
    <h2 className={`text-3xl md:text-4xl font-bold mb-4 ${light ? 'text-white' : 'text-slate-800'}`}>{title}</h2>
    {subtitle && <p className={`text-lg ${light ? 'text-slate-300' : 'text-slate-500'}`}>{subtitle}</p>}
    <div className={`h-1 w-20 mx-auto mt-6 rounded-full ${light ? 'bg-emerald-500' : 'bg-emerald-500'}`}></div>
  </div>
);

// --- Visual Components ---

const CorrelationNetwork = () => {
  const radius = 120;
  const center = 160;
  
  const getNodePos = (angle) => {
    const rad = (angle - 90) * (Math.PI / 180);
    return {
      x: center + radius * Math.cos(rad),
      y: center + radius * Math.sin(rad)
    };
  };

  return (
    <div className="relative w-full h-[320px] flex items-center justify-center">
      <svg width="320" height="320" viewBox="0 0 320 320">
        <defs>
           <marker id="arrow" markerWidth="10" markerHeight="10" refX="20" refY="3" orient="auto" markerUnits="strokeWidth">
             <path d="M0,0 L0,6 L9,3 z" fill="#cbd5e1" />
           </marker>
        </defs>
        
        {chordLinks.map((link, i) => {
          const sourceNode = chordNodes.find(n => n.id === link.source);
          const targetNode = chordNodes.find(n => n.id === link.target);
          const start = getNodePos(sourceNode.angle);
          const end = getNodePos(targetNode.angle);
          return (
            <g key={i}>
              <path d={`M${start.x},${start.y} Q${center},${center} ${end.x},${end.y}`} fill="none" stroke={sourceNode.color} strokeWidth={link.width} opacity="0.3" />
              <text x={(start.x+end.x)/2} y={(start.y+end.y)/2} fontSize="10" fill="#64748b" textAnchor="middle" dy="-5" bg="white">{link.value}</text>
            </g>
          );
        })}

        {chordNodes.map((node, i) => {
          const pos = getNodePos(node.angle);
          return (
            <g key={i} className="cursor-pointer hover:scale-110 transition-transform">
              <circle cx={pos.x} cy={pos.y} r="24" fill="white" stroke={node.color} strokeWidth="3" />
              <text x={pos.x} y={pos.y} dy="4" textAnchor="middle" fontSize="11" fontWeight="bold" fill="#334155">{node.label}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

const DumbbellChart = () => {
  return (
    <div className="flex flex-col space-y-6">
      {dumbbellData.map((item, idx) => (
        <div key={idx} className="relative">
          <div className="flex justify-between text-sm text-slate-500 mb-2">
            <span className="font-medium text-slate-700">{item.category}</span>
          </div>
          <div className="relative h-8 flex items-center">
            <div className="absolute left-0 right-0 top-1/2 h-1 bg-slate-100 rounded"></div>
            <div 
              className="absolute h-1 bg-slate-300 rounded"
              style={{
                left: `${(Math.min(item.undergraduate, item.master, item.phd) - 3) / 2 * 100}%`,
                width: `${(Math.max(item.undergraduate, item.master, item.phd) - Math.min(item.undergraduate, item.master, item.phd)) / 2 * 100}%`
              }}
            ></div>
            <div 
              className="absolute w-4 h-4 rounded-full bg-blue-400 border-2 border-white shadow z-10"
              style={{ left: `${(item.undergraduate - 3) / 2 * 100}%`, top: '50%', transform: 'translate(-50%, -50%)' }}
              title={`本科: ${item.undergraduate}`}
            ></div>
             <div 
              className="absolute w-4 h-4 rounded-full bg-indigo-500 border-2 border-white shadow z-10"
              style={{ left: `${(item.master - 3) / 2 * 100}%`, top: '50%', transform: 'translate(-50%, -50%)' }}
              title={`硕士: ${item.master}`}
            ></div>
            <div 
              className="absolute w-6 h-6 rounded-full bg-rose-500 border-2 border-white shadow flex items-center justify-center text-[8px] text-white font-bold z-20"
              style={{ left: `${(item.phd - 3) / 2 * 100}%`, top: '50%', transform: 'translate(-50%, -50%)' }}
              title={`博士: ${item.phd}`}
            >
              PhD
            </div>
          </div>
        </div>
      ))}
      <div className="flex justify-center gap-6 text-xs text-slate-500 mt-2">
        <div className="flex items-center"><div className="w-2 h-2 rounded-full bg-blue-400 mr-1"></div>本科生</div>
        <div className="flex items-center"><div className="w-2 h-2 rounded-full bg-indigo-500 mr-1"></div>硕士生</div>
        <div className="flex items-center"><div className="w-2 h-2 rounded-full bg-rose-500 mr-1"></div>博士生</div>
      </div>
    </div>
  );
};

const PathDiagram = () => {
  return (
    <div className="relative w-full h-[350px] bg-slate-50 rounded-xl overflow-hidden flex items-center justify-center select-none">
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#cbd5e1" />
          </marker>
        </defs>
        <line x1="15%" y1="50%" x2="40%" y2="30%" stroke="#cbd5e1" strokeWidth="2" markerEnd="url(#arrowhead)" strokeDasharray="5,5" />
        <line x1="15%" y1="50%" x2="40%" y2="70%" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="4,4" opacity="0.5" />
        <line x1="50%" y1="30%" x2="75%" y2="30%" stroke="#ef4444" strokeWidth="3" markerEnd="url(#arrowhead)" />
        <line x1="50%" y1="30%" x2="50%" y2="60%" stroke="#ef4444" strokeWidth="3" markerEnd="url(#arrowhead)" />
        <line x1="85%" y1="30%" x2="85%" y2="45%" stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrowhead)" />
        <line x1="60%" y1="70%" x2="80%" y2="55%" stroke="#3b82f6" strokeWidth="3" markerEnd="url(#arrowhead)" />
      </svg>
      <div className="absolute left-[5%] top-1/2 -translate-y-1/2 w-24 h-24 bg-indigo-100 border-2 border-indigo-200 rounded-full flex flex-col items-center justify-center text-center shadow-sm z-10">
        <BookOpen size={18} className="text-indigo-500 mb-1" />
        <span className="font-bold text-sm text-indigo-800">认知</span>
      </div>
      <div className="absolute left-[40%] top-[20%] w-28 h-20 bg-rose-100 border-2 border-rose-200 rounded-xl flex flex-col items-center justify-center text-center shadow-md z-10 hover:shadow-lg transition-all animate-pulse-slow">
        <Shield size={18} className="text-rose-500 mb-1" />
        <span className="font-bold text-sm text-rose-800">信任 (中介)</span>
        <span className="text-[10px] text-rose-600">β = 0.379**</span>
      </div>
      <div className="absolute left-[40%] bottom-[20%] w-28 h-20 bg-gray-100 border-2 border-gray-200 rounded-xl flex flex-col items-center justify-center text-center shadow-sm z-10">
        <Activity size={18} className="text-gray-500 mb-1" />
        <span className="font-bold text-sm text-gray-800">态度</span>
      </div>
      <div className="absolute right-[15%] top-[20%] w-28 h-20 bg-blue-100 border-2 border-blue-200 rounded-xl flex flex-col items-center justify-center text-center shadow-sm z-10">
        <FileText size={18} className="text-blue-500 mb-1" />
        <span className="font-bold text-sm text-blue-800">政策认同</span>
        <span className="text-[10px] text-blue-600">β = 0.265*</span>
      </div>
      <div className="absolute right-[5%] top-1/2 -translate-y-1/2 w-24 h-24 bg-emerald-100 border-2 border-emerald-200 rounded-full flex flex-col items-center justify-center text-center shadow-lg z-10 border-4 border-emerald-300">
        <MousePointer2 size={18} className="text-emerald-600 mb-1" />
        <span className="font-bold text-sm text-emerald-800">购买意愿</span>
      </div>
    </div>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 selection:bg-emerald-100 selection:text-emerald-900">
      
      <NavBar />

      {/* --- 1. Hero Section --- */}
      <section className="relative bg-slate-900 text-white pt-32 pb-24 px-6 overflow-hidden">
        {/* Background Gradients */}
        <div className="absolute top-0 right-0 w-1/2 h-full bg-emerald-500/10 blur-[100px] pointer-events-none"></div>
        <div className="absolute bottom-0 left-0 w-1/3 h-2/3 bg-blue-500/10 blur-[100px] pointer-events-none"></div>

        <div className="max-w-6xl mx-auto relative z-10">
          <div className="inline-flex items-center space-x-2 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-full px-4 py-1.5 mb-6 text-emerald-400 text-xs font-semibold tracking-wider uppercase">
            <Zap size={14} />
            <span>Research Report 2024</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">
            能源转型背景下<br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-200">
              大学生能源认知与 EV 态度
            </span>
          </h1>
          <p className="text-slate-300 max-w-2xl text-lg md:text-xl leading-relaxed mb-10">
            从“知识驱动”到“制度信任”的范式转变。本研究通过对 75 名中国大学生的实证分析，揭示了 Z 世代在“碳中和”愿景下的绿色决策机制。
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <button 
              onClick={() => document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' })}
              className="bg-emerald-500 hover:bg-emerald-600 text-white px-8 py-4 rounded-lg font-bold transition-all shadow-lg shadow-emerald-500/25 flex items-center justify-center gap-2 group"
            >
              探索数据可视化 <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-8 py-4 rounded-lg font-medium transition-all border border-slate-700 flex items-center justify-center gap-2">
              <FileText size={18} />
              下载完整论文 PDF
            </button>
          </div>
        </div>
      </section>

      {/* --- 2. Background Section (New) --- */}
      <section id="background" className="py-20 px-6 bg-white">
        <div className="max-w-6xl mx-auto">
          <SectionTitle 
            title="研究背景" 
            subtitle="全球能源系统正经历一场深刻而系统性的转型，交通电气化是核心驱动力。" 
          />
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
             <div className="space-y-6">
               <div className="flex items-start space-x-4">
                 <div className="bg-indigo-100 p-3 rounded-lg text-indigo-600">
                   <Globe size={24} />
                 </div>
                 <div>
                   <h3 className="font-bold text-lg text-slate-900">全球气候目标</h3>
                   <p className="text-slate-600 mt-2 leading-relaxed">
                     根据国际可再生能源署 (IRENA) 《2023年世界能源转型展望》，为实现温升控制在 <strong>1.5°C</strong> 以内的目标，交通系统的电气化变革刻不容缓。
                   </p>
                 </div>
               </div>
               <div className="flex items-start space-x-4">
                 <div className="bg-rose-100 p-3 rounded-lg text-rose-600">
                   <Activity size={24} />
                 </div>
                 <div>
                   <h3 className="font-bold text-lg text-slate-900">交通部门排放</h3>
                   <p className="text-slate-600 mt-2 leading-relaxed">
                     交通运输约占全球 CO₂ 排放总量的 <strong>1/4</strong>。推广新能源汽车 (EVs) 不仅是技术升级，更是深度脱碳的核心路径。
                   </p>
                 </div>
               </div>
               <div className="flex items-start space-x-4">
                 <div className="bg-emerald-100 p-3 rounded-lg text-emerald-600">
                   <Users size={24} />
                 </div>
                 <div>
                   <h3 className="font-bold text-lg text-slate-900">为什么关注大学生？</h3>
                   <p className="text-slate-600 mt-2 leading-relaxed">
                     作为未来的消费主力军，大学生正处于从学校步入社会的人生转折点。他们的认知与态度，将深刻预示未来几十年的社会交通模式。
                   </p>
                 </div>
               </div>
             </div>
             
             <div className="bg-slate-50 rounded-2xl p-8 border border-slate-100 relative overflow-hidden group">
               <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-[50px] pointer-events-none group-hover:bg-indigo-500/20 transition-all"></div>
               <h3 className="text-xl font-bold mb-6 text-slate-800">研究问题 (Research Questions)</h3>
               <ul className="space-y-4">
                 {[
                   '大学生的能源认知是否直接决定了购买意愿？',
                   '在集体主义文化背景下，"制度信任"扮演了什么角色？',
                   '性别、专业等人口统计学变量是否仍造成显著差异？'
                 ].map((q, i) => (
                   <li key={i} className="flex items-center space-x-3 bg-white p-4 rounded-lg shadow-sm border border-slate-100">
                     <span className="bg-indigo-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold">{i+1}</span>
                     <span className="text-slate-700 font-medium">{q}</span>
                   </li>
                 ))}
               </ul>
             </div>
          </div>
        </div>
      </section>

      {/* --- 3. Methodology Section (New) --- */}
      <section id="methodology" className="py-20 px-6 bg-slate-50 border-y border-slate-200">
        <div className="max-w-6xl mx-auto">
          <SectionTitle 
            title="研究方法" 
            subtitle="采用定量研究方法，结合多种统计工具进行深度分析。" 
          />
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
            {[
              { label: '样本量', val: '75', icon: Users, sub: '中国大学生群体' },
              { label: '专业构成', val: '83%', icon: BookOpen, sub: '理工科背景主导' },
              { label: '分析工具', val: 'SEM', icon: Network, sub: '结构方程模型' },
              { label: '降维分析', val: 'PCA', icon: BarChart2, sub: '主成分分析' },
            ].map((item, i) => (
              <Card key={i} className="flex flex-col items-center text-center py-8">
                <div className="bg-slate-100 p-3 rounded-full mb-4 text-slate-600">
                  <item.icon size={24} />
                </div>
                <div className="text-3xl font-bold text-slate-800 mb-1">{item.val}</div>
                <div className="text-sm font-bold text-slate-600">{item.label}</div>
                <div className="text-xs text-slate-400 mt-1">{item.sub}</div>
              </Card>
            ))}
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
            <h3 className="text-lg font-bold mb-6 text-slate-800 flex items-center">
              <Search className="mr-2 text-indigo-500"/> 研究架构与变量定义
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="space-y-2">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">自变量 (IV)</span>
                <div className="p-4 bg-indigo-50 rounded-lg border border-indigo-100 text-indigo-900 font-medium">
                  能源认知 (Knowledge)
                </div>
                <p className="text-xs text-slate-500">对能源转型、EV技术原理的基础了解程度。</p>
              </div>
              <div className="space-y-2">
                 <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">中介变量 (Mediator)</span>
                 <div className="p-4 bg-rose-50 rounded-lg border border-rose-100 text-rose-900 font-medium">
                   制度信任 & 责任感
                 </div>
                 <p className="text-xs text-slate-500">对国家政策的认同、对技术的信心、环境责任感。</p>
              </div>
              <div className="space-y-2">
                 <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">因变量 (DV)</span>
                 <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-100 text-emerald-900 font-medium">
                   购买意愿 (Intention)
                 </div>
                 <p className="text-xs text-slate-500">未来购买新能源汽车的可能性。</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* --- 4. Main Dashboard (Existing) --- */}
      <section id="dashboard" className="py-20 px-6 bg-white scroll-mt-20">
        <div className="max-w-6xl mx-auto">
           <SectionTitle 
            title="数据探索" 
            subtitle="交互式图表揭示核心发现。点击下方标签切换视角。" 
          />

          {/* Tabs Navigation */}
          <div className="flex justify-center mb-10">
            <div className="inline-flex bg-slate-100 p-1 rounded-xl">
              {[
                { id: 'overview', label: '核心机制 (SEM)' },
                { id: 'deep-dive', label: '深度分析 (PCA)' },
                { id: 'demographics', label: '群体特征' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-6 py-3 rounded-lg font-medium text-sm transition-all ${
                    activeTab === tab.id 
                      ? 'bg-white text-emerald-600 shadow-sm' 
                      : 'text-slate-500 hover:text-slate-700'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* --- Tab Content --- */}
          <div className="min-h-[500px]">
            {activeTab === 'overview' && (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-2">
                    <Card className="h-full">
                       <div className="flex justify-between items-center mb-6">
                         <h3 className="font-bold text-lg text-slate-800">路径分析模型 (SEM)</h3>
                         <span className="text-xs font-mono bg-slate-100 px-2 py-1 rounded text-slate-500">Model Fit: Good</span>
                       </div>
                       <PathDiagram />
                       <div className="mt-6 p-4 bg-indigo-50/50 rounded-lg border border-indigo-100 text-sm text-slate-700">
                         <strong className="text-indigo-700">关键路径：</strong> 知识 → 信任 (β=0.22) → 意愿 (β=0.45)。这表明知识主要通过增强信任来间接影响意愿，直接影响微乎其微。
                       </div>
                    </Card>
                  </div>
                  <div className="lg:col-span-1 space-y-6">
                    <div className="bg-slate-900 text-white rounded-xl p-6 shadow-xl relative overflow-hidden">
                       <div className="relative z-10">
                         <h4 className="text-emerald-400 font-bold uppercase text-xs tracking-wider mb-2">Insight #1</h4>
                         <h3 className="text-xl font-bold mb-3">信任替代认知</h3>
                         <p className="text-slate-300 text-sm leading-relaxed">
                           中介效应占比高达 <strong>76.2%</strong>。在面对复杂技术时，学生并非依赖技术细节，而是依赖对“国家战略”的信任来做出判断。
                         </p>
                       </div>
                    </div>
                    <Card>
                      <h4 className="font-bold text-slate-800 mb-4 text-sm">风险阻碍排行</h4>
                      <div className="h-[200px]">
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart layout="vertical" data={riskData} margin={{ left: 0, right: 30 }}>
                            <XAxis type="number" hide />
                            <YAxis dataKey="name" type="category" width={70} tick={{fontSize: 11}} />
                            <Tooltip cursor={{fill: 'transparent'}} />
                            <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
                              {riskData.map((entry, index) => (
                                <cell key={`cell-${index}`} fill={entry.impact < 0 ? '#94a3b8' : '#f43f5e'} />
                              ))}
                            </Bar>
                          </BarChart>
                        </ResponsiveContainer>
                      </div>
                    </Card>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'deep-dive' && (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 grid grid-cols-1 md:grid-cols-2 gap-8">
                <Card>
                  <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                    <Network className="mr-2 text-indigo-500" size={20}/> 变量关联网络
                  </h3>
                  <CorrelationNetwork />
                  <p className="text-center text-xs text-slate-500 mt-4">“信任”处于网络的中心枢纽位置，连接政策与态度。</p>
                </Card>
                <Card>
                  <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                    <BarChart2 className="mr-2 text-rose-500" size={20}/> 意识空间分布 (PCA)
                  </h3>
                  <div className="h-[320px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" dataKey="x" name="信任倾向" tick={false} axisLine={false} />
                        <YAxis type="number" dataKey="y" name="责任倾向" tick={false} axisLine={false} />
                        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                        <ReferenceLine y={0} stroke="#cbd5e1" />
                        <ReferenceLine x={0} stroke="#cbd5e1" />
                        <Scatter name="高意愿" data={pcaData.filter(d=>d.type.includes('High'))} fill="#f87171" />
                        <Scatter name="中意愿" data={pcaData.filter(d=>d.type.includes('Med'))} fill="#fbbf24" />
                        <Scatter name="低意愿" data={pcaData.filter(d=>d.type.includes('Low'))} fill="#94a3b8" />
                      </ScatterChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="text-xs text-center text-slate-500 mt-2">
                    X轴：低信任 → 高信任 | Y轴：低责任 → 高责任
                  </div>
                </Card>
              </div>
            )}

            {activeTab === 'demographics' && (
              <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 grid grid-cols-1 md:grid-cols-2 gap-8">
                <Card className="flex flex-col items-center">
                   <h3 className="font-bold text-slate-800 mb-2">性别同质性</h3>
                   <div className="h-[350px] w-full">
                     <ResponsiveContainer width="100%" height="100%">
                        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={genderRadarData}>
                          <PolarGrid stroke="#e2e8f0" />
                          <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11 }} />
                          <PolarRadiusAxis angle={30} domain={[0, 5]} tick={false} axisLine={false} />
                          <Radar name="男性" dataKey="A" stroke="#3b82f6" strokeWidth={2} fill="#3b82f6" fillOpacity={0.2} />
                          <Radar name="女性" dataKey="B" stroke="#ec4899" strokeWidth={2} fill="#ec4899" fillOpacity={0.2} />
                          <Legend />
                          <Tooltip />
                        </RadarChart>
                      </ResponsiveContainer>
                   </div>
                   <p className="text-sm text-slate-500">图形高度重叠，表明在绿色议题上不存在显著的性别鸿沟。</p>
                </Card>
                <Card>
                   <h3 className="font-bold text-slate-800 mb-8">学历影响 (哑铃图)</h3>
                   <DumbbellChart />
                   <div className="mt-8 bg-amber-50 p-4 rounded-lg border border-amber-100">
                     <h4 className="font-bold text-amber-800 text-sm mb-1">💡 发现</h4>
                     <p className="text-amber-700 text-xs">博士群体在“政策支持”和“技术信任”上得分显著更高，显示出高学历与高制度信任的正相关性。</p>
                   </div>
                </Card>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* --- 5. Conclusions Section (New) --- */}
      <section id="conclusion" className="py-20 px-6 bg-slate-900 text-white">
        <div className="max-w-6xl mx-auto">
          <SectionTitle 
            title="结论与启示" 
            subtitle="从理论发现到政策建议的转化。" 
            light={true}
          />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700 hover:border-emerald-500/50 transition-colors">
              <div className="bg-emerald-500/10 w-12 h-12 rounded-lg flex items-center justify-center text-emerald-400 mb-6">
                <Shield size={24} />
              </div>
              <h3 className="text-xl font-bold mb-4">信任构建机制</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                对于大众传播，无需过分纠结于晦涩的技术参数。更有效的策略是建立<strong>“国家背书”</strong>和<strong>“基础设施透明化”</strong>，从而增强制度信任。
              </p>
            </div>
            <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700 hover:border-blue-500/50 transition-colors">
              <div className="bg-blue-500/10 w-12 h-12 rounded-lg flex items-center justify-center text-blue-400 mb-6">
                <Users size={24} />
              </div>
              <h3 className="text-xl font-bold mb-4">代际共识</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                Z 世代已形成超越性别与专业的<strong>全球绿色共识</strong>。营销应利用这一“代际同质性”，将 EV 塑造为一种符合其身份认同的文化符号。
              </p>
            </div>
            <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700 hover:border-rose-500/50 transition-colors">
              <div className="bg-rose-500/10 w-12 h-12 rounded-lg flex items-center justify-center text-rose-400 mb-6">
                <Target size={24} />
              </div>
              <h3 className="text-xl font-bold mb-4">痛点精准打击</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                数据明确显示，<strong>“充电不便”</strong>对意愿的杀伤力远超“里程焦虑”。政策重心应从提升单车续航转向完善充电网络的可及性。
              </p>
            </div>
          </div>

          <div className="text-center">
            <p className="text-slate-500 text-sm mb-6">© 2024 能源转型与大学生认知研究小组 | 基于真实调研数据构建</p>
          </div>
        </div>
      </section>
    </div>
  );
}