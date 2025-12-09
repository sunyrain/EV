import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ScatterChart, Scatter, ReferenceLine, ComposedChart, Line, Area, AreaChart, Sankey
} from 'recharts';
import { 
  BookOpen, Users, Zap, Shield, TrendingUp, 
  Activity, MousePointer2, FileText, Share2, Target, GitCommit,
  Network, BarChart2, Globe, Search, Lightbulb, ChevronDown, Menu, X, ArrowRight,
  CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';

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

// 1.4 风险数据 (Composed Chart Data)
const riskData = [
  { name: '高昂价格', impact: -0.26, worry: 17, label: '17%' },
  { name: '里程焦虑', impact: -0.21, worry: 59, label: '59%' },
  { name: '充电不便', impact: -0.40, worry: 67, label: '67%' },
  { name: '电池安全', impact: 0.28, worry: 72, label: '72%' },
  { name: '整体安全', impact: 0.01, worry: 72, label: '72%' },
];

// 1.7 Ridgeline Data (Simulated)
const ridgelineData = Array.from({ length: 50 }, (_, i) => {
  const x = 1.5 + (i / 50) * 4; // 1.5 to 5.5
  return {
    x: x.toFixed(1),
    knowledge: Math.exp(-Math.pow(x - 3.91, 2) / 0.8) * 0.8 + Math.random() * 0.05,
    responsibility: Math.exp(-Math.pow(x - 3.76, 2) / 1.2) * 0.6 + Math.exp(-Math.pow(x - 5.0, 2) / 0.5) * 0.4,
    trust: Math.exp(-Math.pow(x - 4.19, 2) / 0.6) * 0.9 + Math.exp(-Math.pow(x - 5.2, 2) / 0.4) * 0.3,
    policy: Math.exp(-Math.pow(x - 4.23, 2) / 0.5) * 0.7 + Math.exp(-Math.pow(x - 5.0, 2) / 0.4) * 0.5,
  };
});

// 1.8 Sankey Data
const sankeyData = {
  nodes: [
    { name: '非常不了解' }, { name: '不了解' }, { name: '中立' }, { name: '了解' }, { name: '非常了解' },
    { name: '非常不可能' }, { name: '不可能' }, { name: '不确定' }, { name: '可能' }, { name: '非常可能' }
  ],
  links: [
    { source: 0, target: 5, value: 1 },
    { source: 1, target: 6, value: 4 }, { source: 1, target: 7, value: 2 },
    { source: 2, target: 6, value: 2 }, { source: 2, target: 7, value: 15 }, { source: 2, target: 8, value: 10 }, { source: 2, target: 9, value: 5 },
    { source: 3, target: 7, value: 5 }, { source: 3, target: 8, value: 12 }, { source: 3, target: 9, value: 7 },
    { source: 4, target: 8, value: 3 }, { source: 4, target: 9, value: 9 }
  ]
};

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

// --- 动画配置 (Animations) ---
const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } }
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15
    }
  }
};

const scaleIn = {
  hidden: { scale: 0.9, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { duration: 0.5 } }
};

// --- 组件部分 (Components) ---

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
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
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-white/80 backdrop-blur-md shadow-sm py-3 border-b border-slate-200/50' : 'bg-transparent py-6'}`}
    >
      <div className="max-w-7xl mx-auto px-6 flex justify-between items-center">
        <div className={`font-bold text-xl flex items-center space-x-2 ${scrolled ? 'text-slate-800' : 'text-white'}`}>
          <div className="bg-emerald-500 p-1.5 rounded-lg text-white">
            <Zap size={20} fill="currentColor" />
          </div>
          <span className="tracking-tight">EV Research <span className="font-light opacity-80">2024</span></span>
        </div>
        
        {/* Desktop Menu */}
        <div className={`hidden md:flex space-x-1 font-medium ${scrolled ? 'text-slate-600' : 'text-slate-200'}`}>
          {['背景', '方法', '数据探索', '结论'].map((item, idx) => {
             const ids = ['background', 'methodology', 'dashboard', 'conclusion'];
             return (
               <button 
                 key={item} 
                 onClick={() => scrollTo(ids[idx])}
                 className={`px-4 py-2 rounded-full transition-all hover:bg-emerald-500/10 hover:text-emerald-500 ${scrolled ? '' : 'hover:bg-white/10 hover:text-white'}`}
               >
                 {item}
               </button>
             )
          })}
        </div>

        {/* Mobile Menu Button */}
        <button className="md:hidden text-emerald-500 p-2" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="absolute top-full left-0 right-0 bg-white shadow-lg border-t border-slate-100 overflow-hidden md:hidden"
          >
            <div className="p-4 flex flex-col space-y-2">
              {['背景', '方法', '数据探索', '结论'].map((item, idx) => {
                const ids = ['background', 'methodology', 'dashboard', 'conclusion'];
                return (
                  <button 
                    key={item} 
                    onClick={() => scrollTo(ids[idx])}
                    className="text-left text-slate-600 font-medium py-3 px-4 rounded-lg hover:bg-slate-50 active:bg-slate-100"
                  >
                    {item}
                  </button>
                )
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

const Card = ({ children, className = "", delay = 0 }) => (
  <motion.div 
    variants={fadeInUp}
    whileHover={{ y: -5, shadow: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)" }}
    className={`bg-white rounded-2xl shadow-sm border border-slate-100 p-6 transition-shadow duration-300 ${className}`}
  >
    {children}
  </motion.div>
);

const SectionTitle = ({ title, subtitle, light = false }) => (
  <motion.div 
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true, margin: "-100px" }}
    variants={fadeInUp}
    className="mb-16 text-center max-w-3xl mx-auto"
  >
    <h2 className={`text-3xl md:text-5xl font-bold mb-6 tracking-tight ${light ? 'text-white' : 'text-slate-900'}`}>{title}</h2>
    {subtitle && <p className={`text-lg md:text-xl leading-relaxed ${light ? 'text-slate-300' : 'text-slate-500'}`}>{subtitle}</p>}
    <div className={`h-1.5 w-24 mx-auto mt-8 rounded-full ${light ? 'bg-emerald-500' : 'bg-gradient-to-r from-emerald-500 to-teal-400'}`}></div>
  </motion.div>
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
            <motion.g 
              key={i}
              initial={{ pathLength: 0, opacity: 0 }}
              whileInView={{ pathLength: 1, opacity: 0.3 }}
              transition={{ duration: 1, delay: i * 0.1 }}
            >
              <path d={`M${start.x},${start.y} Q${center},${center} ${end.x},${end.y}`} fill="none" stroke={sourceNode.color} strokeWidth={link.width} />
              <text x={(start.x+end.x)/2} y={(start.y+end.y)/2} fontSize="10" fill="#64748b" textAnchor="middle" dy="-5" bg="white">{link.value}</text>
            </motion.g>
          );
        })}

        {chordNodes.map((node, i) => {
          const pos = getNodePos(node.angle);
          return (
            <motion.g 
              key={i} 
              className="cursor-pointer"
              whileHover={{ scale: 1.2 }}
              initial={{ scale: 0 }}
              whileInView={{ scale: 1 }}
              transition={{ type: "spring", stiffness: 260, damping: 20, delay: 0.5 + i * 0.1 }}
            >
              <circle cx={pos.x} cy={pos.y} r="24" fill="white" stroke={node.color} strokeWidth="3" className="drop-shadow-sm" />
              <text x={pos.x} y={pos.y} dy="4" textAnchor="middle" fontSize="11" fontWeight="bold" fill="#334155">{node.label}</text>
            </motion.g>
          );
        })}
      </svg>
    </div>
  );
};

const DumbbellChart = () => {
  return (
    <div className="flex flex-col space-y-8">
      {dumbbellData.map((item, idx) => (
        <motion.div 
          key={idx} 
          className="relative"
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          transition={{ delay: idx * 0.1 }}
        >
          <div className="flex justify-between text-sm text-slate-500 mb-3">
            <span className="font-bold text-slate-700">{item.category}</span>
          </div>
          <div className="relative h-8 flex items-center group">
            <div className="absolute left-0 right-0 top-1/2 h-1.5 bg-slate-100 rounded-full"></div>
            <motion.div 
              className="absolute h-1.5 bg-slate-300 rounded-full"
              initial={{ width: 0 }}
              whileInView={{ 
                left: `${(Math.min(item.undergraduate, item.master, item.phd) - 3) / 2 * 100}%`,
                width: `${(Math.max(item.undergraduate, item.master, item.phd) - Math.min(item.undergraduate, item.master, item.phd)) / 2 * 100}%`
              }}
              transition={{ duration: 1, delay: 0.5 }}
            ></motion.div>
            
            {[
              { val: item.undergraduate, color: 'bg-blue-400', label: '本科' },
              { val: item.master, color: 'bg-indigo-500', label: '硕士' },
              { val: item.phd, color: 'bg-rose-500', label: '博士' }
            ].map((point, pIdx) => (
              <motion.div 
                key={pIdx}
                className={`absolute w-4 h-4 rounded-full ${point.color} border-2 border-white shadow-md z-10 cursor-help transition-transform hover:scale-150`}
                initial={{ left: '0%' }}
                whileInView={{ left: `${(point.val - 3) / 2 * 100}%` }}
                transition={{ duration: 1, delay: 0.2 }}
                style={{ top: '50%', transform: 'translate(-50%, -50%)' }}
              >
                <div className="opacity-0 group-hover:opacity-100 absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-slate-800 text-white text-xs rounded whitespace-nowrap pointer-events-none transition-opacity z-50">
                  {point.label}: {point.val}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      ))}
      <div className="flex justify-center gap-6 text-xs text-slate-500 mt-2 pt-4 border-t border-slate-100">
        <div className="flex items-center"><div className="w-3 h-3 rounded-full bg-blue-400 mr-2"></div>本科生</div>
        <div className="flex items-center"><div className="w-3 h-3 rounded-full bg-indigo-500 mr-2"></div>硕士生</div>
        <div className="flex items-center"><div className="w-3 h-3 rounded-full bg-rose-500 mr-2"></div>博士生</div>
      </div>
    </div>
  );
};

const PathDiagram = () => {
  // Animation variants for lines
  const lineVariant = {
    hidden: { pathLength: 0, opacity: 0 },
    visible: (custom) => ({
      pathLength: 1,
      opacity: 1,
      transition: { duration: 0.8, delay: custom, ease: "easeInOut" }
    })
  };

  // Animation variants for nodes
  const nodeVariant = {
    hidden: { scale: 0, opacity: 0 },
    visible: (custom) => ({
      scale: 1,
      opacity: 1,
      transition: { duration: 0.5, delay: custom, type: "spring", stiffness: 200 }
    })
  };

  return (
    <div className="relative w-full h-[450px] bg-slate-50/50 rounded-xl overflow-hidden flex items-center justify-center select-none border border-slate-100">
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
          </marker>
          <marker id="arrowhead-active" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#f87171" />
          </marker>
          <marker id="arrowhead-negative" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#818cf8" />
          </marker>
        </defs>
        
        {/* 1. Knowledge -> Trust (Dashed, Positive) */}
        <motion.line 
          x1="20%" y1="50%" x2="40%" y2="25%" 
          stroke="#fca5a5" strokeWidth="2" markerEnd="url(#arrowhead-active)" strokeDasharray="5,5"
          variants={lineVariant} initial="hidden" whileInView="visible" custom={0.3}
        />
        <text x="28%" y="35%" fill="#f87171" fontSize="10">β=0.22</text>

        {/* 2. Knowledge -> Responsibility (Dashed, Positive) */}
        <motion.line 
          x1="20%" y1="50%" x2="40%" y2="75%" 
          stroke="#fca5a5" strokeWidth="2" markerEnd="url(#arrowhead-active)" strokeDasharray="5,5"
          variants={lineVariant} initial="hidden" whileInView="visible" custom={0.3}
        />
        <text x="28%" y="65%" fill="#f87171" fontSize="10">β=0.23</text>

        {/* 3. Knowledge -> Attitude (Dashed, Positive) */}
        <motion.path 
          d="M 200 225 Q 350 225 580 320" // Approximate curve
          fill="none" stroke="#fca5a5" strokeWidth="1" markerEnd="url(#arrowhead-active)" strokeDasharray="5,5"
          initial={{ pathLength: 0, opacity: 0 }} whileInView={{ pathLength: 1, opacity: 1 }} transition={{ duration: 1, delay: 0.3 }}
        />
        <text x="35%" y="52%" fill="#f87171" fontSize="10">β=0.15</text>
        
        {/* 4. Trust -> Policy (Solid, Positive) */}
        <motion.line 
          x1="50%" y1="25%" x2="70%" y2="35%" 
          stroke="#f87171" strokeWidth="3" markerEnd="url(#arrowhead-active)" 
          variants={lineVariant} initial="hidden" whileInView="visible" custom={1.1}
        />
        <text x="60%" y="28%" fill="#f87171" fontSize="10" fontWeight="bold">β=0.54***</text>

        {/* 5. Trust -> Attitude (Solid, Positive) */}
        <motion.line 
          x1="50%" y1="25%" x2="70%" y2="65%" 
          stroke="#f87171" strokeWidth="3" markerEnd="url(#arrowhead-active)" 
          variants={lineVariant} initial="hidden" whileInView="visible" custom={1.1}
        />
        <text x="60%" y="45%" fill="#f87171" fontSize="10" fontWeight="bold">β=0.52***</text>

        {/* 6. Trust -> Intention (Solid, Positive) */}
        <motion.path 
          d="M 500 112 Q 700 150 850 225" 
          fill="none" stroke="#f87171" strokeWidth="2" markerEnd="url(#arrowhead-active)" 
          initial={{ pathLength: 0, opacity: 0 }} whileInView={{ pathLength: 1, opacity: 1 }} transition={{ duration: 1, delay: 1.1 }}
        />
        
        {/* 7. Responsibility -> Attitude (Solid, Positive) */}
        <motion.line 
          x1="50%" y1="75%" x2="70%" y2="65%" 
          stroke="#f87171" strokeWidth="2" markerEnd="url(#arrowhead-active)" 
          variants={lineVariant} initial="hidden" whileInView="visible" custom={1.1}
        />
        <text x="60%" y="72%" fill="#f87171" fontSize="10">β=0.27*</text>

        {/* 8. Policy -> Intention (Solid, Negative) */}
        <motion.line 
          x1="80%" y1="35%" x2="90%" y2="45%" 
          stroke="#818cf8" strokeWidth="3" markerEnd="url(#arrowhead-negative)" 
          variants={lineVariant} initial="hidden" whileInView="visible" custom={1.9}
        />
        <text x="85%" y="38%" fill="#818cf8" fontSize="10" fontWeight="bold">β=-0.49***</text>

        {/* 9. Attitude -> Intention (Solid, Negative) */}
        <motion.line 
          x1="80%" y1="65%" x2="90%" y2="55%" 
          stroke="#818cf8" strokeWidth="3" markerEnd="url(#arrowhead-negative)" 
          variants={lineVariant} initial="hidden" whileInView="visible" custom={1.9}
        />
        <text x="85%" y="62%" fill="#818cf8" fontSize="10" fontWeight="bold">β=-0.45***</text>
      </svg>

      {/* Node 1: Knowledge (Left) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={0}
        className="absolute left-[10%] top-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-20 bg-indigo-200/50 border-2 border-indigo-300 rounded-xl flex flex-col items-center justify-center text-center shadow-sm z-10"
      >
        <BookOpen size={18} className="text-indigo-600 mb-1" />
        <span className="font-bold text-sm text-indigo-900">Knowledge</span>
      </motion.div>
      
      {/* Node 2: Trust (Top Middle) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={0.8}
        className="absolute left-[40%] top-[25%] -translate-x-1/2 -translate-y-1/2 w-32 h-24 bg-rose-400 border-2 border-rose-500 rounded-2xl flex flex-col items-center justify-center text-center shadow-lg z-10 text-white"
      >
        <Shield size={20} className="text-white mb-1" />
        <span className="font-bold text-sm">Trust</span>
      </motion.div>

      {/* Node 3: Responsibility (Bottom Middle) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={0.8}
        className="absolute left-[40%] top-[75%] -translate-x-1/2 -translate-y-1/2 w-32 h-24 bg-orange-300 border-2 border-orange-400 rounded-2xl flex flex-col items-center justify-center text-center shadow-sm z-10 text-white"
      >
        <Users size={20} className="text-white mb-1" />
        <span className="font-bold text-sm">Responsibility</span>
      </motion.div>

      {/* Node 4: Policy (Right Top) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={1.6}
        className="absolute left-[70%] top-[35%] -translate-x-1/2 -translate-y-1/2 w-28 h-20 bg-slate-200 border-2 border-slate-300 rounded-xl flex flex-col items-center justify-center text-center shadow-sm z-10"
      >
        <FileText size={18} className="text-slate-600 mb-1" />
        <span className="font-bold text-sm text-slate-800">Policy</span>
      </motion.div>

      {/* Node 5: Attitude (Right Bottom) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={1.6}
        className="absolute left-[70%] top-[65%] -translate-x-1/2 -translate-y-1/2 w-28 h-20 bg-slate-200 border-2 border-slate-300 rounded-xl flex flex-col items-center justify-center text-center shadow-sm z-10"
      >
        <Activity size={18} className="text-slate-600 mb-1" />
        <span className="font-bold text-sm text-slate-800">Attitude</span>
      </motion.div>

      {/* Node 6: Intention (Far Right) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={2.2}
        className="absolute left-[90%] top-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-24 bg-red-400 border-4 border-red-300 rounded-2xl flex flex-col items-center justify-center text-center shadow-xl z-10 text-white"
      >
        <MousePointer2 size={24} className="text-white mb-1" />
        <span className="font-bold text-sm">Intention</span>
      </motion.div>
    </div>
  );
};

const RidgelineChart = () => {
  return (
    <div className="h-[400px] w-full flex flex-col -space-y-12">
      {['Knowledge Index', 'Responsibility Index', 'Trust Index', 'Policy Support Index'].map((key, idx) => {
        const colors = ['#818cf8', '#f43f5e', '#fb923c', '#94a3b8'];
        const dataKey = key.split(' ')[0].toLowerCase();
        return (
          <div key={key} className="h-[120px] w-full relative">
             <ResponsiveContainer width="100%" height="100%">
               <AreaChart data={ridgelineData}>
                 <defs>
                   <linearGradient id={`color${idx}`} x1="0" y1="0" x2="0" y2="1">
                     <stop offset="5%" stopColor={colors[idx]} stopOpacity={0.8}/>
                     <stop offset="95%" stopColor={colors[idx]} stopOpacity={0}/>
                   </linearGradient>
                 </defs>
                 <Area 
                   type="monotone" 
                   dataKey={dataKey} 
                   stroke={colors[idx]} 
                   fillOpacity={1} 
                   fill={`url(#color${idx})`} 
                 />
               </AreaChart>
             </ResponsiveContainer>
             <div className="absolute top-10 left-0 text-xs font-bold" style={{ color: colors[idx] }}>{key}</div>
          </div>
        )
      })}
      <div className="h-8 border-t border-slate-200 mt-12 flex justify-between text-xs text-slate-400 px-4 pt-2">
        <span>1.5</span><span>2.5</span><span>3.5</span><span>4.5</span><span>5.5</span>
      </div>
    </div>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 selection:bg-emerald-100 selection:text-emerald-900 overflow-x-hidden">
      
      <NavBar />

      {/* --- 1. Hero Section --- */}
      <section className="relative bg-slate-900 text-white pt-40 pb-32 px-6 overflow-hidden">
        {/* Animated Background Elements */}
        <motion.div 
          animate={{ scale: [1, 1.2, 1], opacity: [0.1, 0.2, 0.1] }}
          transition={{ duration: 8, repeat: Infinity }}
          className="absolute top-0 right-0 w-[800px] h-[800px] bg-emerald-500/10 rounded-full blur-[120px] pointer-events-none -translate-y-1/2 translate-x-1/3"
        />
        <motion.div 
          animate={{ scale: [1, 1.1, 1], opacity: [0.1, 0.15, 0.1] }}
          transition={{ duration: 10, repeat: Infinity, delay: 1 }}
          className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-500/10 rounded-full blur-[100px] pointer-events-none translate-y-1/3 -translate-x-1/4"
        />

        <div className="max-w-6xl mx-auto relative z-10">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center space-x-2 bg-slate-800/80 backdrop-blur-md border border-slate-700 rounded-full px-4 py-1.5 mb-8 text-emerald-400 text-xs font-bold tracking-widest uppercase shadow-lg"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>Research Report 2024</span>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-5xl md:text-7xl font-extrabold leading-tight mb-8 tracking-tight"
          >
            能源转型背景下<br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-200 to-cyan-400">
              大学生能源认知与 EV 态度
            </span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-slate-300 max-w-2xl text-lg md:text-xl leading-relaxed mb-12 font-light"
          >
            从“知识驱动”到“制度信任”的范式转变。本研究通过对 75 名中国大学生的实证分析，揭示了 Z 世代在“碳中和”愿景下的绿色决策机制。
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <button 
              onClick={() => document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' })}
              className="bg-emerald-500 hover:bg-emerald-400 text-slate-900 px-8 py-4 rounded-full font-bold transition-all shadow-[0_0_20px_rgba(16,185,129,0.3)] hover:shadow-[0_0_30px_rgba(16,185,129,0.5)] flex items-center justify-center gap-2 group"
            >
              探索数据可视化 <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="bg-white/5 hover:bg-white/10 text-white px-8 py-4 rounded-full font-medium transition-all border border-white/10 backdrop-blur-sm flex items-center justify-center gap-2 hover:border-white/30">
              <FileText size={18} />
              下载完整论文 PDF
            </button>
          </motion.div>
        </div>
      </section>

      {/* --- 2. Background Section --- */}
      <section id="background" className="py-24 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <SectionTitle 
            title="研究背景" 
            subtitle="全球能源系统正经历一场深刻而系统性的转型，交通电气化是核心驱动力。" 
          />
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
             <motion.div 
               variants={staggerContainer}
               initial="hidden"
               whileInView="visible"
               viewport={{ once: true }}
               className="space-y-8"
             >
               {[
                 { icon: Globe, color: 'text-indigo-600', bg: 'bg-indigo-50', title: '全球气候目标', desc: '根据国际可再生能源署 (IRENA) 《2023年世界能源转型展望》，为实现温升控制在 1.5°C 以内的目标，交通系统的电气化变革刻不容缓。' },
                 { icon: Activity, color: 'text-rose-600', bg: 'bg-rose-50', title: '交通部门排放', desc: '交通运输约占全球 CO₂ 排放总量的 1/4。推广新能源汽车 (EVs) 不仅是技术升级，更是深度脱碳的核心路径。' },
                 { icon: Users, color: 'text-emerald-600', bg: 'bg-emerald-50', title: '为什么关注大学生？', desc: '作为未来的消费主力军，大学生正处于从学校步入社会的人生转折点。他们的认知与态度，将深刻预示未来几十年的社会交通模式。' }
               ].map((item, i) => (
                 <motion.div key={i} variants={fadeInUp} className="flex items-start space-x-5 group">
                   <div className={`${item.bg} p-4 rounded-2xl ${item.color} group-hover:scale-110 transition-transform duration-300 shadow-sm`}>
                     <item.icon size={28} />
                   </div>
                   <div>
                     <h3 className="font-bold text-xl text-slate-900 mb-2">{item.title}</h3>
                     <p className="text-slate-600 leading-relaxed">
                       {item.desc}
                     </p>
                   </div>
                 </motion.div>
               ))}
             </motion.div>
             
             <motion.div 
               initial={{ opacity: 0, x: 50 }}
               whileInView={{ opacity: 1, x: 0 }}
               viewport={{ once: true }}
               transition={{ duration: 0.8 }}
               className="bg-slate-50 rounded-3xl p-10 border border-slate-100 relative overflow-hidden group hover:shadow-2xl transition-shadow duration-500"
             >
               <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full blur-[80px] pointer-events-none group-hover:bg-indigo-500/10 transition-all"></div>
               <h3 className="text-2xl font-bold mb-8 text-slate-800 flex items-center">
                 <Search className="mr-3 text-indigo-500" /> 研究问题 (Research Questions)
               </h3>
               <ul className="space-y-4 relative z-10">
                 {[
                   '大学生的能源认知是否直接决定了购买意愿？',
                   '在集体主义文化背景下，"制度信任"扮演了什么角色？',
                   '性别、专业等人口统计学变量是否仍造成显著差异？'
                 ].map((q, i) => (
                   <motion.li 
                     key={i} 
                     initial={{ opacity: 0, x: 20 }}
                     whileInView={{ opacity: 1, x: 0 }}
                     transition={{ delay: 0.2 + i * 0.1 }}
                     className="flex items-center space-x-4 bg-white p-5 rounded-xl shadow-sm border border-slate-100 hover:border-indigo-200 transition-colors"
                   >
                     <span className="bg-indigo-500 text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shadow-md shadow-indigo-200">{i+1}</span>
                     <span className="text-slate-700 font-medium text-lg">{q}</span>
                   </motion.li>
                 ))}
               </ul>
             </motion.div>
          </div>
        </div>
      </section>

      {/* --- 3. Methodology Section --- */}
      <section id="methodology" className="py-24 px-6 bg-slate-50 border-y border-slate-200">
        <div className="max-w-7xl mx-auto">
          <SectionTitle 
            title="研究方法" 
            subtitle="采用定量研究方法，结合多种统计工具进行深度分析。" 
          />
          
          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16"
          >
            {[
              { label: '样本量', val: '75', icon: Users, sub: '中国大学生群体' },
              { label: '专业构成', val: '83%', icon: BookOpen, sub: '理工科背景主导' },
              { label: '分析工具', val: 'SEM', icon: Network, sub: '结构方程模型' },
              { label: '降维分析', val: 'PCA', icon: BarChart2, sub: '主成分分析' },
            ].map((item, i) => (
              <Card key={i} className="flex flex-col items-center text-center py-10 hover:border-emerald-200">
                <div className="bg-slate-100 p-4 rounded-full mb-5 text-slate-600 group-hover:bg-emerald-50 group-hover:text-emerald-600 transition-colors">
                  <item.icon size={32} />
                </div>
                <div className="text-4xl font-extrabold text-slate-800 mb-2 tracking-tight">{item.val}</div>
                <div className="text-sm font-bold text-slate-600 uppercase tracking-wide">{item.label}</div>
                <div className="text-xs text-slate-400 mt-2">{item.sub}</div>
              </Card>
            ))}
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="bg-white rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100 p-10"
          >
            <h3 className="text-xl font-bold mb-8 text-slate-800 flex items-center">
              <GitCommit className="mr-3 text-indigo-500"/> 研究架构与变量定义
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-10 relative">
              {/* Connecting Line for Desktop */}
              <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-gradient-to-r from-indigo-200 via-rose-200 to-emerald-200 -z-10"></div>

              <div className="space-y-4 text-center md:text-left">
                <span className="inline-block px-3 py-1 rounded-full bg-slate-100 text-xs font-bold text-slate-500 uppercase tracking-wider">自变量 (IV)</span>
                <div className="p-6 bg-indigo-50 rounded-2xl border border-indigo-100 text-indigo-900 font-bold text-lg shadow-sm">
                  能源认知 (Knowledge)
                </div>
                <p className="text-sm text-slate-500 leading-relaxed">对能源转型、EV技术原理的基础了解程度。</p>
              </div>
              <div className="space-y-4 text-center md:text-left">
                 <span className="inline-block px-3 py-1 rounded-full bg-slate-100 text-xs font-bold text-slate-500 uppercase tracking-wider">中介变量 (Mediator)</span>
                 <div className="p-6 bg-rose-50 rounded-2xl border border-rose-100 text-rose-900 font-bold text-lg shadow-sm">
                   制度信任 & 责任感
                 </div>
                 <p className="text-sm text-slate-500 leading-relaxed">对国家政策的认同、对技术的信心、环境责任感。</p>
              </div>
              <div className="space-y-4 text-center md:text-left">
                 <span className="inline-block px-3 py-1 rounded-full bg-slate-100 text-xs font-bold text-slate-500 uppercase tracking-wider">因变量 (DV)</span>
                 <div className="p-6 bg-emerald-50 rounded-2xl border border-emerald-100 text-emerald-900 font-bold text-lg shadow-sm">
                   购买意愿 (Intention)
                 </div>
                 <p className="text-sm text-slate-500 leading-relaxed">未来购买新能源汽车的可能性。</p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* --- 4. Main Dashboard --- */}
      <section id="dashboard" className="py-24 px-6 bg-white scroll-mt-20">
        <div className="max-w-7xl mx-auto">
           <SectionTitle 
            title="数据探索" 
            subtitle="交互式图表揭示核心发现。点击下方标签切换视角。" 
          />

          {/* Tabs Navigation */}
          <div className="flex justify-center mb-12">
            <div className="inline-flex bg-slate-100 p-1.5 rounded-2xl relative">
              {[
                { id: 'overview', label: '核心机制 (SEM)' },
                { id: 'deep-dive', label: '深度分析 (PCA)' },
                { id: 'demographics', label: '群体特征' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative px-8 py-3 rounded-xl font-bold text-sm transition-colors z-10 ${
                    activeTab === tab.id ? 'text-emerald-700' : 'text-slate-500 hover:text-slate-700'
                  }`}
                >
                  {activeTab === tab.id && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute inset-0 bg-white shadow-sm rounded-xl border border-slate-200/50"
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  <span className="relative z-10">{tab.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* --- Tab Content --- */}
          <div className="min-h-[600px]">
            <AnimatePresence mode="wait">
              {activeTab === 'overview' && (
                <motion.div 
                  key="overview"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4 }}
                  className="space-y-8"
                >
                  {/* Row 1: SEM Path Diagram (Full Width) */}
                  <Card className="w-full">
                     <div className="flex justify-between items-center mb-8">
                       <h3 className="font-bold text-xl text-slate-800 flex items-center">
                         <Network className="mr-2 text-emerald-500"/> 路径分析模型 (SEM)
                       </h3>
                       <span className="text-xs font-mono bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full border border-emerald-100">Model Fit: Good (RMSEA=0.04)</span>
                     </div>
                     <div className="w-full flex items-center justify-center bg-slate-50/30 rounded-xl border border-slate-100/50 p-4">
                        <PathDiagram />
                     </div>
                     <div className="mt-6 p-4 bg-indigo-50/50 rounded-xl border border-indigo-100 text-sm text-slate-700 leading-relaxed flex items-start gap-3">
                       <Lightbulb className="text-indigo-600 shrink-0 mt-0.5" size={18} />
                       <div>
                         <strong className="text-indigo-700 block mb-1">关键路径发现：</strong> 
                         知识 → 信任 (β=0.22) → 意愿 (β=0.45)。这表明知识主要通过增强信任来间接影响意愿，直接影响微乎其微。
                       </div>
                     </div>
                  </Card>

                  {/* Row 2: Insights & Risk Chart */}
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-1">
                      <motion.div 
                        whileHover={{ scale: 1.02 }}
                        className="h-full bg-slate-900 text-white rounded-3xl p-8 shadow-2xl shadow-slate-900/20 relative overflow-hidden flex flex-col justify-center"
                      >
                         <div className="absolute top-0 right-0 w-40 h-40 bg-emerald-500/20 rounded-full blur-[50px] pointer-events-none"></div>
                         <div className="relative z-10">
                           <h4 className="text-emerald-400 font-bold uppercase text-xs tracking-wider mb-3 flex items-center">
                             <Lightbulb size={14} className="mr-1"/> Insight #1
                           </h4>
                           <h3 className="text-2xl font-bold mb-4">信任替代认知</h3>
                           <p className="text-slate-300 text-sm leading-relaxed">
                             中介效应占比高达 <strong>76.2%</strong>。在面对复杂技术时，学生并非依赖技术细节，而是依赖对“国家战略”的信任来做出判断。
                           </p>
                         </div>
                      </motion.div>
                    </div>
                    
                    <div className="lg:col-span-2">
                      <Card className="h-full">
                        <h4 className="font-bold text-slate-800 mb-6 text-sm flex items-center">
                          <Target className="mr-2 text-rose-500"/> 风险阻碍排行 (Worry vs Intention Diff)
                        </h4>
                        <div className="h-[300px]">
                          <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart
                              layout="vertical"
                              data={riskData}
                              margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                            >
                              <CartesianGrid stroke="#f5f5f5" horizontal={false} />
                              <XAxis type="number" domain={[-0.5, 0.5]} tickCount={5} />
                              <YAxis dataKey="name" type="category" scale="band" width={80} tick={{fontSize: 11}} />
                              <Tooltip />
                              <Legend />
                              <Bar dataKey="worry" barSize={20} fill="#cbd5e1" name="Worry % (Scaled)" background={{ fill: '#eee' }} />
                              <Scatter name="Intention Diff" dataKey="impact" fill="#f43f5e" shape="diamond" />
                            </ComposedChart>
                          </ResponsiveContainer>
                        </div>
                        <div className="text-[10px] text-slate-400 text-center mt-2">
                          * Bar length represents Worry %. Diamond position represents Intention Difference.
                        </div>
                      </Card>
                    </div>
                  </div>
                </motion.div>
              )}

              {activeTab === 'deep-dive' && (
                <motion.div 
                  key="deep-dive"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4 }}
                  className="grid grid-cols-1 md:grid-cols-2 gap-8"
                >
                  <Card>
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                      <Share2 className="mr-2 text-indigo-500" size={20}/> 变量关联网络
                    </h3>
                    <CorrelationNetwork />
                    <p className="text-center text-xs text-slate-500 mt-6 bg-slate-50 py-2 rounded-lg">“信任”处于网络的中心枢纽位置，连接政策与态度。</p>
                  </Card>
                  <Card>
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                      <BarChart2 className="mr-2 text-rose-500" size={20}/> 意识空间分布 (PCA)
                    </h3>
                    <div className="h-[320px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                          <XAxis type="number" dataKey="x" name="信任倾向" tick={false} axisLine={false} />
                          <YAxis type="number" dataKey="y" name="责任倾向" tick={false} axisLine={false} />
                          <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ borderRadius: '8px' }} />
                          <ReferenceLine y={0} stroke="#cbd5e1" />
                          <ReferenceLine x={0} stroke="#cbd5e1" />
                          <Scatter name="高意愿" data={pcaData.filter(d=>d.type.includes('High'))} fill="#f87171" />
                          <Scatter name="中意愿" data={pcaData.filter(d=>d.type.includes('Med'))} fill="#fbbf24" />
                          <Scatter name="低意愿" data={pcaData.filter(d=>d.type.includes('Low'))} fill="#94a3b8" />
                        </ScatterChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="text-xs text-center text-slate-500 mt-4 flex justify-center gap-4">
                      <span className="flex items-center"><div className="w-2 h-2 bg-red-400 rounded-full mr-1"></div> 高意愿</span>
                      <span className="flex items-center"><div className="w-2 h-2 bg-amber-400 rounded-full mr-1"></div> 中意愿</span>
                      <span className="flex items-center"><div className="w-2 h-2 bg-slate-400 rounded-full mr-1"></div> 低意愿</span>
                    </div>
                  </Card>
                </motion.div>
              )}

              {activeTab === 'demographics' && (
                <motion.div 
                  key="demographics"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4 }}
                  className="grid grid-cols-1 md:grid-cols-2 gap-8"
                >
                  <Card className="col-span-1 md:col-span-2">
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                      <Activity className="mr-2 text-indigo-500"/> 核心变量分布 (Ridgeline Plot)
                    </h3>
                    <RidgelineChart />
                  </Card>

                  <Card className="flex flex-col items-center">
                     <h3 className="font-bold text-slate-800 mb-4 w-full text-left flex items-center">
                       <Users className="mr-2 text-blue-500"/> 性别同质性
                     </h3>
                     <div className="h-[350px] w-full">
                       <ResponsiveContainer width="100%" height="100%">
                          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={genderRadarData}>
                            <PolarGrid stroke="#e2e8f0" />
                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11 }} />
                            <PolarRadiusAxis angle={30} domain={[0, 5]} tick={false} axisLine={false} />
                            <Radar name="男性" dataKey="A" stroke="#3b82f6" strokeWidth={2} fill="#3b82f6" fillOpacity={0.2} />
                            <Radar name="女性" dataKey="B" stroke="#ec4899" strokeWidth={2} fill="#ec4899" fillOpacity={0.2} />
                            <Legend />
                            <Tooltip contentStyle={{ borderRadius: '8px' }} />
                          </RadarChart>
                        </ResponsiveContainer>
                     </div>
                     <p className="text-sm text-slate-500 bg-blue-50 px-4 py-2 rounded-lg">图形高度重叠，表明在绿色议题上不存在显著的性别鸿沟。</p>
                  </Card>
                  <Card>
                     <h3 className="font-bold text-slate-800 mb-8 flex items-center">
                       <BookOpen className="mr-2 text-amber-500"/> 学历影响 (哑铃图)
                     </h3>
                     <DumbbellChart />
                     <div className="mt-8 bg-amber-50 p-5 rounded-xl border border-amber-100 flex items-start gap-3">
                       <Lightbulb className="text-amber-600 shrink-0 mt-0.5" size={18} />
                       <div>
                         <h4 className="font-bold text-amber-800 text-sm mb-1">发现</h4>
                         <p className="text-amber-700 text-xs leading-relaxed">博士群体在“政策支持”和“技术信任”上得分显著更高，显示出高学历与高制度信任的正相关性。</p>
                       </div>
                     </div>
                  </Card>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </section>

      {/* --- 5. Conclusions Section --- */}
      <section id="conclusion" className="py-24 px-6 bg-slate-900 text-white relative overflow-hidden">
        {/* Background decoration */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-emerald-500/5 rounded-full blur-[100px]"></div>
          <div className="absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] bg-blue-500/5 rounded-full blur-[100px]"></div>
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <SectionTitle 
            title="结论与启示" 
            subtitle="从理论发现到政策建议的转化。" 
            light={true}
          />

          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16"
          >
            <motion.div variants={fadeInUp} className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-emerald-500/50 transition-all hover:bg-slate-800 group">
              <div className="bg-emerald-500/10 w-14 h-14 rounded-2xl flex items-center justify-center text-emerald-400 mb-6 group-hover:scale-110 transition-transform">
                <Shield size={28} />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">信任构建机制</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                对于大众传播，无需过分纠结于晦涩的技术参数。更有效的策略是建立<strong>“国家背书”</strong>和<strong>“基础设施透明化”</strong>，从而增强制度信任。
              </p>
            </motion.div>
            <motion.div variants={fadeInUp} className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-blue-500/50 transition-all hover:bg-slate-800 group">
              <div className="bg-blue-500/10 w-14 h-14 rounded-2xl flex items-center justify-center text-blue-400 mb-6 group-hover:scale-110 transition-transform">
                <Users size={28} />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">代际共识</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                Z 世代已形成超越性别与专业的<strong>全球绿色共识</strong>。营销应利用这一“代际同质性”，将 EV 塑造为一种符合其身份认同的文化符号。
              </p>
            </motion.div>
            <motion.div variants={fadeInUp} className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-rose-500/50 transition-all hover:bg-slate-800 group">
              <div className="bg-rose-500/10 w-14 h-14 rounded-2xl flex items-center justify-center text-rose-400 mb-6 group-hover:scale-110 transition-transform">
                <Target size={28} />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">痛点精准打击</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                数据明确显示，<strong>“充电不便”</strong>对意愿的杀伤力远超“里程焦虑”。政策重心应从提升单车续航转向完善充电网络的可及性。
              </p>
            </motion.div>
          </motion.div>

          <div className="text-center border-t border-slate-800 pt-12">
            <p className="text-slate-500 text-sm mb-2">© 2024 能源转型与大学生认知研究小组 | 基于真实调研数据构建</p>
            <p className="text-slate-600 text-xs">Designed with React & Tailwind CSS</p>
          </div>
        </div>
      </section>
    </div>
  );
}
