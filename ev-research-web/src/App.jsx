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

// Import static images
import semPathImg from './assets/Advanced_SEM_Path.png';
import riskIntentionImg from './assets/Advanced_Risk_Intention.png';
import sankeyImg from './assets/Advanced_Sankey_Knowledge_to_Intention.png';
import variableChordImg from './assets/Advanced_Variable_Chord.png';
import ridgelineImg from './assets/Advanced_Ridgeline_Core_Indices.png';
import pcaImg from './assets/Advanced_Awareness_PCA.png';

// --- 1. Data Section ---

// Color Scheme (consistent with charts)
const COLORS = {
  primary: '#B6B3D6',      // Cool Purple-Grey
  primaryLight: '#CFCFE3',
  neutral: '#D5D3DE',      // Light Grey
  neutralMid: '#D5D1D1',
  warmLight: '#F6DFD6',    // Light Coral Pink
  warm: '#F8B2A2',
  warmDeep: '#F1837A',
  accent: '#E9687A',       // Deep Red-Pink
};

// 1.1 Sample Distribution
const demographicsData = [
  { name: 'Male', value: 47, fill: '#B6B3D6' },
  { name: 'Female', value: 28, fill: '#E9687A' },
];

// 1.2 Education Differences (Dumbbell Data)
const dumbbellData = [
  { category: 'Policy Support', undergraduate: 4.15, master: 4.17, phd: 4.41 },
  { category: 'Tech Trust', undergraduate: 4.00, master: 4.22, phd: 4.41 },
  { category: 'Responsibility', undergraduate: 3.56, master: 3.90, phd: 3.92 },
  { category: 'Knowledge', undergraduate: 3.81, master: 3.98, phd: 3.99 },
];

// 1.3 Radar Chart Data (Gender Comparison)
const genderRadarData = [
  { subject: 'Tech Trust', A: 4.04, B: 4.36, fullMark: 5 },
  { subject: 'EV Tech Awareness', A: 3.86, B: 4.13, fullMark: 5 },
  { subject: 'Policy Execution', A: 4.21, B: 4.14, fullMark: 5 },
  { subject: 'Policy Support', A: 4.50, B: 4.43, fullMark: 5 },
  { subject: 'Oil Restriction', A: 4.18, B: 3.91, fullMark: 5 },
];

// 1.4 Risk Data (Composed Chart Data)
const riskData = [
  { name: 'High Price', impact: -0.26, worry: 17, label: '17%' },
  { name: 'Range Anxiety', impact: -0.21, worry: 59, label: '59%' },
  { name: 'Charging Inconvenience', impact: -0.40, worry: 67, label: '67%' },
  { name: 'Battery Safety', impact: 0.28, worry: 72, label: '72%' },
  { name: 'Overall Safety', impact: 0.01, worry: 72, label: '72%' },
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
    { name: 'Very Unfamiliar' }, { name: 'Unfamiliar' }, { name: 'Neutral' }, { name: 'Familiar' }, { name: 'Very Familiar' },
    { name: 'Very Unlikely' }, { name: 'Unlikely' }, { name: 'Uncertain' }, { name: 'Likely' }, { name: 'Very Likely' }
  ],
  links: [
    { source: 0, target: 5, value: 1 },
    { source: 1, target: 6, value: 4 }, { source: 1, target: 7, value: 2 },
    { source: 2, target: 6, value: 2 }, { source: 2, target: 7, value: 15 }, { source: 2, target: 8, value: 10 }, { source: 2, target: 9, value: 5 },
    { source: 3, target: 7, value: 5 }, { source: 3, target: 8, value: 12 }, { source: 3, target: 9, value: 7 },
    { source: 4, target: 8, value: 3 }, { source: 4, target: 9, value: 9 }
  ]
};

// 1.5 PCA Scatter Plot Simulated Data
const pcaData = [
  { x: 2.5, y: 1.1, type: 'High Intention', fill: '#E9687A' }, 
  { x: 1.8, y: 0.8, type: 'High Intention', fill: '#E9687A' },
  { x: 2.1, y: -0.5, type: 'High Intention', fill: '#E9687A' },
  { x: 1.2, y: -2.0, type: 'High Intention', fill: '#E9687A' },
  { x: 0.5, y: -1.5, type: 'High Intention', fill: '#E9687A' },
  { x: 0.2, y: 0.8, type: 'Medium Intention', fill: '#F8B2A2' },
  { x: -0.5, y: 0.5, type: 'Medium Intention', fill: '#F8B2A2' },
  { x: -1.2, y: 1.2, type: 'Medium Intention', fill: '#F8B2A2' },
  { x: -1.5, y: -0.8, type: 'Low Intention', fill: '#B6B3D6' },
  { x: -2.0, y: 0.2, type: 'Low Intention', fill: '#B6B3D6' },
  { x: -0.8, y: -2.2, type: 'Low Intention', fill: '#B6B3D6' },
  { x: -2.5, y: -0.3, type: 'Low Intention', fill: '#B6B3D6' },
];

// 1.6 Correlation Chord Diagram Data
const chordNodes = [
  { id: 'Trust', label: 'Trust', color: '#E9687A', angle: 0 },
  { id: 'Policy', label: 'Policy', color: '#B6B3D6', angle: 60 },
  { id: 'Attitude', label: 'Attitude', color: '#D5D3DE', angle: 120 },
  { id: 'Intention', label: 'Intention', color: '#F1837A', angle: 180 },
  { id: 'Know', label: 'Knowledge', color: '#CFCFE3', angle: 240 },
  { id: 'Resp', label: 'Responsibility', color: '#F8B2A2', angle: 300 },
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

// --- Animation Config ---
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

// --- Components ---

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
          <div className="bg-[#E9687A] p-1.5 rounded-lg text-white">
            <Zap size={20} fill="currentColor" />
          </div>
          <span className="tracking-tight">EV Research <span className="font-light opacity-80">2025</span></span>
        </div>
        
        {/* Desktop Menu */}
        <div className={`hidden md:flex space-x-1 font-medium ${scrolled ? 'text-slate-700' : 'text-white/90'}`}>
          {['Background', 'Methods', 'Data Explorer', 'Conclusions'].map((item, idx) => {
             const ids = ['background', 'methodology', 'dashboard', 'conclusion'];
             return (
               <button 
                 key={item} 
                 onClick={() => scrollTo(ids[idx])}
                 className={`px-4 py-2 rounded-full transition-all ${scrolled ? 'hover:bg-[#E9687A]/10 hover:text-[#E9687A]' : 'hover:bg-white/10'}`}
               >
                 {item}
               </button>
             )
          })}
        </div>

        {/* Mobile Menu Button */}
        <button className="md:hidden text-[#E9687A] p-2" onClick={() => setIsOpen(!isOpen)}>
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
              {['Background', 'Methods', 'Data Explorer', 'Conclusions'].map((item, idx) => {
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
    <div className={`h-1.5 w-24 mx-auto mt-8 rounded-full ${light ? 'bg-[#E9687A]' : 'bg-gradient-to-r from-[#B6B3D6] to-[#E9687A]'}`}></div>
  </motion.div>
);

// --- Visual Components ---

const CorrelationNetwork = () => {
  const [hoveredNode, setHoveredNode] = useState(null);
  const radius = 120;
  const center = 160;
  
  const getNodePos = (angle) => {
    const rad = (angle - 90) * (Math.PI / 180);
    return {
      x: center + radius * Math.cos(rad),
      y: center + radius * Math.sin(rad)
    };
  };

  // Calculate label position to avoid overlap
  const getLabelOffset = (link, sourcePos, targetPos) => {
    const midX = (sourcePos.x + targetPos.x) / 2;
    const midY = (sourcePos.y + targetPos.y) / 2;
    // Calculate direction from center to midpoint of link, offset label outwards
    const dirX = midX - center;
    const dirY = midY - center;
    const dist = Math.sqrt(dirX * dirX + dirY * dirY);
    const offsetDist = 25; // Offset distance
    return {
      x: midX + (dirX / dist) * offsetDist,
      y: midY + (dirY / dist) * offsetDist
    };
  };

  // Check if link is related to current hovered node
  const isLinkHighlighted = (link) => {
    if (!hoveredNode) return false;
    return link.source === hoveredNode || link.target === hoveredNode;
  };

  // Check if node is related to current hovered node
  const isNodeHighlighted = (nodeId) => {
    if (!hoveredNode) return true;
    if (nodeId === hoveredNode) return true;
    return chordLinks.some(link => 
      (link.source === hoveredNode && link.target === nodeId) ||
      (link.target === hoveredNode && link.source === nodeId)
    );
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
          const labelPos = getLabelOffset(link, start, end);
          const highlighted = isLinkHighlighted(link);
          const dimmed = hoveredNode && !highlighted;
          
          return (
            <motion.g 
              key={i}
              initial={{ pathLength: 0, opacity: 0 }}
              whileInView={{ pathLength: 1, opacity: dimmed ? 0.1 : (highlighted ? 0.8 : 0.3) }}
              animate={{ opacity: dimmed ? 0.1 : (highlighted ? 0.8 : 0.3) }}
              transition={{ duration: 0.3 }}
            >
              <path 
                d={`M${start.x},${start.y} Q${center},${center} ${end.x},${end.y}`} 
                fill="none" 
                stroke={highlighted ? sourceNode.color : sourceNode.color} 
                strokeWidth={highlighted ? link.width + 2 : link.width}
                style={{ filter: highlighted ? 'drop-shadow(0 0 4px rgba(0,0,0,0.3))' : 'none' }}
              />
              <rect 
                x={labelPos.x - 16} 
                y={labelPos.y - 8} 
                width="32" 
                height="16" 
                fill="white" 
                rx="4"
                opacity={dimmed ? 0.3 : 0.9}
              />
              <text 
                x={labelPos.x} 
                y={labelPos.y} 
                fontSize="10" 
                fill={highlighted ? '#1e293b' : '#64748b'} 
                textAnchor="middle" 
                dy="3"
                fontWeight={highlighted ? 'bold' : 'normal'}
                opacity={dimmed ? 0.3 : 1}
              >
                {link.value}
              </text>
            </motion.g>
          );
        })}

        {chordNodes.map((node, i) => {
          const pos = getNodePos(node.angle);
          const isActive = hoveredNode === node.id;
          const isRelated = isNodeHighlighted(node.id);
          const dimmed = hoveredNode && !isRelated;
          
          return (
            <motion.g 
              key={i} 
              className="cursor-pointer"
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              whileHover={{ scale: 1.15 }}
              initial={{ scale: 0 }}
              whileInView={{ scale: 1 }}
              animate={{ 
                opacity: dimmed ? 0.3 : 1,
              }}
              transition={{ type: "spring", stiffness: 260, damping: 20, delay: 0.5 + i * 0.1 }}
            >
              <circle 
                cx={pos.x} 
                cy={pos.y} 
                r={isActive ? 28 : 24} 
                fill="white" 
                stroke={node.color} 
                strokeWidth={isActive ? 4 : 3} 
                className="drop-shadow-sm"
                style={{ 
                  filter: isActive ? `drop-shadow(0 0 8px ${node.color})` : 'none',
                  transition: 'all 0.2s ease'
                }}
              />
              <text 
                x={pos.x} 
                y={pos.y} 
                dy="4" 
                textAnchor="middle" 
                fontSize={isActive ? "12" : "11"} 
                fontWeight="bold" 
                fill={isActive ? node.color : '#334155'}
              >
                {node.label}
              </text>
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
              { val: item.undergraduate, color: 'bg-[#CFCFE3]', label: 'Undergrad' },
              { val: item.master, color: 'bg-[#B6B3D6]', label: 'Master' },
              { val: item.phd, color: 'bg-[#E9687A]', label: 'PhD' }
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
        <div className="flex items-center"><div className="w-3 h-3 rounded-full bg-[#CFCFE3] mr-2"></div>Undergraduate</div>
        <div className="flex items-center"><div className="w-3 h-3 rounded-full bg-[#B6B3D6] mr-2"></div>Master's</div>
        <div className="flex items-center"><div className="w-3 h-3 rounded-full bg-[#E9687A] mr-2"></div>PhD</div>
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
        className="absolute left-[10%] top-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-20 bg-[#CFCFE3]/50 border-2 border-[#B6B3D6] rounded-xl flex flex-col items-center justify-center text-center shadow-sm z-10"
      >
        <BookOpen size={18} className="text-[#B6B3D6] mb-1" />
        <span className="font-bold text-sm text-slate-700">Knowledge</span>
      </motion.div>
      
      {/* Node 2: Trust (Top Middle) */}
      <motion.div 
        variants={nodeVariant} initial="hidden" whileInView="visible" custom={0.8}
        className="absolute left-[40%] top-[25%] -translate-x-1/2 -translate-y-1/2 w-32 h-24 bg-[#E9687A] border-2 border-[#F1837A] rounded-2xl flex flex-col items-center justify-center text-center shadow-lg z-10 text-white"
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
  const [activeTab, setActiveTab] = useState('demographics');

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-800 selection:bg-[#F6DFD6] selection:text-[#E9687A] overflow-x-hidden">
      
      <NavBar />

      {/* --- 1. Hero Section --- */}
      <section className="relative bg-slate-900 text-white pt-40 pb-32 px-6 overflow-hidden">
        {/* Animated Background Elements */}
        <motion.div 
          animate={{ scale: [1, 1.2, 1], opacity: [0.1, 0.2, 0.1] }}
          transition={{ duration: 8, repeat: Infinity }}
          className="absolute top-0 right-0 w-[800px] h-[800px] bg-[#E9687A]/10 rounded-full blur-[120px] pointer-events-none -translate-y-1/2 translate-x-1/3"
        />
        <motion.div 
          animate={{ scale: [1, 1.1, 1], opacity: [0.1, 0.15, 0.1] }}
          transition={{ duration: 10, repeat: Infinity, delay: 1 }}
          className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-[#B6B3D6]/10 rounded-full blur-[100px] pointer-events-none translate-y-1/3 -translate-x-1/4"
        />

        <div className="max-w-6xl mx-auto relative z-10">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center space-x-2 bg-slate-800/80 backdrop-blur-md border border-slate-700 rounded-full px-4 py-1.5 mb-8 text-[#F8B2A2] text-xs font-bold tracking-widest uppercase shadow-lg"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#F8B2A2] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#E9687A]"></span>
            </span>
            <span>Research Report 2025</span>
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-5xl md:text-7xl font-extrabold leading-tight mb-8 tracking-tight"
          >
            Energy Transition Era:<br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#F8B2A2] via-[#F6DFD6] to-[#CFCFE3]">
              College Students' Energy Perception & EV Attitudes
            </span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-slate-300 max-w-2xl text-lg md:text-xl leading-relaxed mb-12 font-light"
          >
            A paradigm shift from "knowledge-driven" to "institutional trust". This study reveals the green decision-making mechanism of Gen Z under the "carbon neutrality" vision through empirical analysis of 75 Chinese university students.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex flex-col sm:flex-row gap-4"
          >
            <button 
              onClick={() => document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' })}
              className="bg-[#E9687A] hover:bg-[#F1837A] text-white px-8 py-4 rounded-full font-bold transition-all shadow-[0_0_20px_rgba(233,104,122,0.3)] hover:shadow-[0_0_30px_rgba(233,104,122,0.5)] flex items-center justify-center gap-2 group"
            >
              Explore Data Visualization <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="bg-white/5 hover:bg-white/10 text-white px-8 py-4 rounded-full font-medium transition-all border border-white/10 backdrop-blur-sm flex items-center justify-center gap-2 hover:border-white/30">
              <FileText size={18} />
              Download Full Paper PDF
            </button>
          </motion.div>
        </div>
      </section>

      {/* --- 2. Background Section --- */}
      <section id="background" className="py-24 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <SectionTitle 
            title="Background" 
            subtitle="The global energy system is undergoing a profound and systemic transformation, with transportation electrification being a core driver." 
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
                 { icon: Globe, color: 'text-[#B6B3D6]', bg: 'bg-[#CFCFE3]/30', title: 'Global Climate Goals', desc: 'According to IRENA\'s "World Energy Transitions Outlook 2023", the electrification of transport is urgent to limit global warming to 1.5°C.' },
                 { icon: Activity, color: 'text-[#E9687A]', bg: 'bg-[#E9687A]/10', title: 'Transport Emissions', desc: 'Transport accounts for ~1/4 of global CO₂ emissions. Promoting EVs is not just a tech upgrade, but a core path to deep decarbonization.' },
                 { icon: Users, color: 'text-[#F1837A]', bg: 'bg-[#F6DFD6]', title: 'Why College Students?', desc: 'As future consumers, students are at a pivotal life stage. Their perceptions and attitudes will deeply foreshadow social transport patterns for decades.' }
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
               <div className="absolute top-0 right-0 w-64 h-64 bg-[#B6B3D6]/5 rounded-full blur-[80px] pointer-events-none group-hover:bg-[#B6B3D6]/10 transition-all"></div>
               <h3 className="text-2xl font-bold mb-8 text-slate-800 flex items-center">
                 <Search className="mr-3 text-[#E9687A]" /> Research Questions
               </h3>
               <ul className="space-y-4 relative z-10">
                 {[
                   'Does students\' energy knowledge directly determine purchase intention?',
                   'What role does "institutional trust" play in a collectivist culture?',
                   'Do demographic variables like gender and major still cause significant differences?'
                 ].map((q, i) => (
                   <motion.li 
                     key={i} 
                     initial={{ opacity: 0, x: 20 }}
                     whileInView={{ opacity: 1, x: 0 }}
                     transition={{ delay: 0.2 + i * 0.1 }}
                     className="flex items-center space-x-4 bg-white p-5 rounded-xl shadow-sm border border-slate-100 hover:border-[#F8B2A2] transition-colors"
                   >
                     <span className="flex-shrink-0 bg-[#E9687A] text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shadow-md shadow-[#F6DFD6]">{i+1}</span>
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
            title="Methodology" 
            subtitle="Adopting quantitative research methods combined with various statistical tools for in-depth analysis." 
          />
          
          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16"
          >
            {[
              { label: 'Sample Size', val: '75', icon: Users, sub: 'Chinese University Students' },
              { label: 'Major Composition', val: '83%', icon: BookOpen, sub: 'STEM Background Dominant' },
              { label: 'Analysis Tool', val: 'SEM', icon: Network, sub: 'Structural Equation Modeling' },
              { label: 'Dim. Reduction', val: 'PCA', icon: BarChart2, sub: 'Principal Component Analysis' },
            ].map((item, i) => (
              <Card key={i} className="flex flex-col items-center text-center py-10 hover:border-[#F8B2A2]">
                <div className="bg-slate-100 p-4 rounded-full mb-5 text-slate-600 group-hover:bg-[#F6DFD6] group-hover:text-[#E9687A] transition-colors">
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
              <GitCommit className="mr-3 text-[#B6B3D6]"/> Research Framework & Variable Definitions
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-10 relative">
              {/* Connecting Line for Desktop */}
              <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-gradient-to-r from-[#CFCFE3] via-[#F8B2A2] to-[#E9687A] -z-10"></div>

              <div className="space-y-4 text-center md:text-left">
                <span className="inline-block px-3 py-1 rounded-full bg-slate-100 text-xs font-bold text-slate-500 uppercase tracking-wider">Independent Variable (IV)</span>
                <div className="p-6 bg-[#CFCFE3]/30 rounded-2xl border border-[#B6B3D6]/30 text-slate-700 font-bold text-lg shadow-sm">
                  Energy Knowledge
                </div>
                <p className="text-sm text-slate-500 leading-relaxed">Basic understanding of energy transition and EV technology principles.</p>
              </div>
              <div className="space-y-4 text-center md:text-left">
                 <span className="inline-block px-3 py-1 rounded-full bg-slate-100 text-xs font-bold text-slate-500 uppercase tracking-wider">Mediator Variable</span>
                 <div className="p-6 bg-[#E9687A]/10 rounded-2xl border border-[#E9687A]/30 text-[#E9687A] font-bold text-lg shadow-sm">
                   Institutional Trust & Responsibility
                 </div>
                 <p className="text-sm text-slate-500 leading-relaxed">Agreement with national policies, confidence in technology, environmental responsibility.</p>
              </div>
              <div className="space-y-4 text-center md:text-left">
                 <span className="inline-block px-3 py-1 rounded-full bg-slate-100 text-xs font-bold text-slate-500 uppercase tracking-wider">Dependent Variable (DV)</span>
                 <div className="p-6 bg-[#F6DFD6] rounded-2xl border border-[#F8B2A2] text-[#F1837A] font-bold text-lg shadow-sm">
                   Purchase Intention
                 </div>
                 <p className="text-sm text-slate-500 leading-relaxed">Likelihood of purchasing new energy vehicles in the future.</p>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* --- 4. Main Dashboard --- */}
      <section id="dashboard" className="py-24 px-6 bg-white scroll-mt-20">
        <div className="max-w-7xl mx-auto">
           <SectionTitle 
            title="Data Exploration" 
            subtitle="Interactive charts reveal core findings. Click tabs below to switch views." 
           />          {/* Tabs Navigation */}
          <div className="flex justify-center mb-12">
            <div className="inline-flex bg-slate-100 p-1.5 rounded-2xl relative gap-2">
              {[
                { id: 'demographics', label: 'Demographics' },
                { id: 'overview', label: 'Core Mechanism' },
                { id: 'deep-dive', label: 'Deep Dive' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`relative px-8 py-3 rounded-xl font-bold text-sm transition-all z-10 ${
                    activeTab === tab.id 
                      ? 'text-[#E9687A] bg-white shadow-sm border border-slate-200/50' 
                      : 'text-slate-500 hover:text-slate-700'
                  }`}
                >
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
                         <Network className="mr-2 text-[#E9687A]"/> Path Analysis Model (SEM)
                       </h3>
                       <span className="text-xs font-mono bg-[#F6DFD6] text-[#E9687A] px-3 py-1 rounded-full border border-[#F8B2A2]">Model Fit: Good (RMSEA=0.04)</span>
                     </div>
                     <div className="w-full flex items-center justify-center bg-white rounded-xl border border-slate-100/50 p-2">
                        <img src={semPathImg} alt="SEM Path Diagram" className="w-full h-auto max-h-[500px] object-contain" />
                     </div>
                     <div className="mt-6 p-4 bg-[#CFCFE3]/30 rounded-xl border border-[#B6B3D6]/30 text-sm text-slate-700 leading-relaxed flex items-start gap-3">
                       <Lightbulb className="text-[#E9687A] shrink-0 mt-0.5" size={18} />
                       <div>
                         <strong className="text-[#E9687A] block mb-1">Key Path Findings:</strong> 
                         Knowledge → Trust (β=0.22) → Intention (β=0.45). This indicates that knowledge mainly affects intention indirectly by enhancing trust, with negligible direct impact.
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
                         <div className="absolute top-0 right-0 w-40 h-40 bg-[#E9687A]/20 rounded-full blur-[50px] pointer-events-none"></div>
                         <div className="relative z-10">
                           <h4 className="text-[#F8B2A2] font-bold uppercase text-xs tracking-wider mb-3 flex items-center">
                             <Lightbulb size={14} className="mr-1"/> Insight #1
                           </h4>
                           <h3 className="text-2xl font-bold mb-4">Trust Replaces Knowledge</h3>
                           <p className="text-slate-300 text-sm leading-relaxed">
                             The mediation effect accounts for <strong>76.2%</strong>. When facing complex technologies, students rely on trust in "national strategy" rather than technical details to make judgments.
                           </p>
                         </div>
                      </motion.div>
                    </div>
                    
                    <div className="lg:col-span-2">
                      <Card className="h-full">
                        <h4 className="font-bold text-slate-800 mb-6 text-sm flex items-center">
                          <Target className="mr-2 text-[#E9687A]"/> Risk Barrier Ranking (Worry vs Intention Diff)
                        </h4>
                        <div className="flex items-center justify-center">
                          <img src={riskIntentionImg} alt="Risk Intention Chart" className="w-full h-auto max-h-[380px] object-contain" />
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
                  className="space-y-8"
                >
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <Card>
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                      <Share2 className="mr-2 text-[#B6B3D6]" size={20}/> Variable Correlation Network
                    </h3>
                    <div className="flex justify-center">
                      <img src={variableChordImg} alt="Variable Correlation Network" className="max-w-full h-auto max-h-[450px] object-contain" />
                    </div>
                    <p className="text-center text-xs text-slate-500 mt-6 bg-slate-50 py-2 rounded-lg">"Trust" is at the central hub of the network, connecting policy and attitude.</p>
                  </Card>
                  <Card>
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                      <BarChart2 className="mr-2 text-[#E9687A]" size={20}/> Consciousness Space Distribution (PCA)
                    </h3>
                    <div className="flex justify-center">
                      <img src={pcaImg} alt="Consciousness Space Distribution (PCA)" className="max-w-full h-auto max-h-[450px] object-contain" />
                    </div>
                  </Card>
                  </div>

                  <Card>
                    <h3 className="font-bold text-slate-800 mb-6 flex items-center">
                      <GitCommit className="mr-2 text-[#E9687A]" size={20}/> Cognition-Intention Flow (Sankey)
                    </h3>
                    <div className="flex items-center justify-center">
                      <img src={sankeyImg} alt="Sankey Flow Chart" className="w-full h-auto max-h-[550px] object-contain" />
                    </div>
                    <p className="text-center text-xs text-slate-500 mt-6 bg-slate-50 py-2 rounded-lg">Shows the flow from different knowledge level groups to purchase intention levels. It can be seen that even among the "Neutral" knowledge group, a significant portion flows to "High Intention", reaffirming the mediating role of trust.</p>
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
                      <Activity className="mr-2 text-[#B6B3D6]"/> Core Variable Distribution (Ridgeline Plot)
                    </h3>
                    <div className="flex justify-center">
                      <img src={ridgelineImg} alt="Core Variable Distribution" className="max-w-full h-auto max-h-[500px] object-contain" />
                    </div>
                  </Card>

                  <Card className="flex flex-col items-center">
                     <h3 className="font-bold text-slate-800 mb-4 w-full text-left flex items-center">
                       <Users className="mr-2 text-[#B6B3D6]"/> Gender Homogeneity
                     </h3>
                     <div className="h-[350px] w-full">
                       <ResponsiveContainer width="100%" height="100%">
                          <RadarChart cx="50%" cy="50%" outerRadius="70%" data={genderRadarData}>
                            <PolarGrid stroke="#e2e8f0" />
                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11 }} />
                            <PolarRadiusAxis angle={30} domain={[0, 5]} tick={false} axisLine={false} />
                            <Radar name="Male" dataKey="A" stroke="#B6B3D6" strokeWidth={2} fill="#B6B3D6" fillOpacity={0.2} />
                            <Radar name="Female" dataKey="B" stroke="#E9687A" strokeWidth={2} fill="#E9687A" fillOpacity={0.2} />
                            <Legend />
                            <Tooltip contentStyle={{ borderRadius: '8px' }} />
                          </RadarChart>
                        </ResponsiveContainer>
                     </div>
                     <p className="text-sm text-slate-500 bg-[#CFCFE3]/30 px-4 py-2 rounded-lg">The graphs overlap significantly, indicating no significant gender gap on green issues.</p>
                  </Card>
                  <Card>
                     <h3 className="font-bold text-slate-800 mb-8 flex items-center">
                       <BookOpen className="mr-2 text-amber-500"/> Education Impact (Dumbbell Chart)
                     </h3>
                     <DumbbellChart />
                     <div className="mt-8 bg-amber-50 p-5 rounded-xl border border-amber-100 flex items-start gap-3">
                       <Lightbulb className="text-amber-600 shrink-0 mt-0.5" size={18} />
                       <div>
                         <h4 className="font-bold text-amber-800 text-sm mb-1">Discovery</h4>
                         <p className="text-amber-700 text-xs leading-relaxed">PhD groups score significantly higher on "Policy Support" and "Tech Trust", showing a positive correlation between higher education and institutional trust.</p>
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
          <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-[#E9687A]/5 rounded-full blur-[100px]"></div>
          <div className="absolute bottom-[-10%] left-[-5%] w-[500px] h-[500px] bg-[#B6B3D6]/5 rounded-full blur-[100px]"></div>
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          <SectionTitle 
            title="Conclusions & Implications" 
            subtitle="Translating theoretical findings into policy recommendations." 
            light={true}
          />

          <motion.div 
            variants={staggerContainer}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16"
          >
            <motion.div variants={fadeInUp} className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-[#E9687A]/50 transition-all hover:bg-slate-800 group">
              <div className="bg-[#E9687A]/10 w-14 h-14 rounded-2xl flex items-center justify-center text-[#F8B2A2] mb-6 group-hover:scale-110 transition-transform">
                <Shield size={28} />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">Trust Building Mechanism</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                For mass communication, there is no need to dwell on obscure technical parameters. A more effective strategy is to establish <strong>"National Endorsement"</strong> and <strong>"Infrastructure Transparency"</strong> to enhance institutional trust.
              </p>
            </motion.div>
            <motion.div variants={fadeInUp} className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-blue-500/50 transition-all hover:bg-slate-800 group">
              <div className="bg-[#B6B3D6]/10 w-14 h-14 rounded-2xl flex items-center justify-center text-[#B6B3D6] mb-6 group-hover:scale-110 transition-transform">
                <Users size={28} />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">Generational Consensus</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                Gen Z has formed a <strong>global green consensus</strong> transcending gender and major. Marketing should leverage this "generational homogeneity" to shape EVs as a cultural symbol aligning with their identity.
              </p>
            </motion.div>
            <motion.div variants={fadeInUp} className="bg-slate-800/50 backdrop-blur-sm p-8 rounded-3xl border border-slate-700 hover:border-[#F8B2A2]/50 transition-all hover:bg-slate-800 group">
              <div className="bg-[#F8B2A2]/10 w-14 h-14 rounded-2xl flex items-center justify-center text-[#F8B2A2] mb-6 group-hover:scale-110 transition-transform">
                <Target size={28} />
              </div>
              <h3 className="text-xl font-bold mb-4 text-white">Precise Pain Point Targeting</h3>
              <p className="text-slate-400 leading-relaxed text-sm">
                Data clearly shows that <strong>"Charging Inconvenience"</strong> has a far greater negative impact on intention than "Range Anxiety". Policy focus should shift from increasing vehicle range to improving charging network accessibility.
              </p>
            </motion.div>
          </motion.div>

          <div className="text-center border-t border-slate-800 pt-12">
            <p className="text-slate-500 text-sm mb-2">© 2025 Energy Transition & Student Perception Research Group | Built on Real Survey Data</p>
            <p className="text-slate-600 text-xs">Designed with React & Tailwind CSS</p>
          </div>
        </div>
      </section>
    </div>
  );
}
