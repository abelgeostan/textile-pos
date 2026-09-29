import{ReactNode,useState}from'react';import{Link,useLocation}from'react-router-dom';import{BarChart3,Box,FileText,LogOut,Menu,RotateCcw,ShoppingCart,Truck,Users,X,Home,MoreHorizontal}from'lucide-react';import{logout,getUser}from'../lib/auth';

const mobileLinks=[
 ['Home','/admin/mobile',Home],
 ['Products','/admin/mobile/products',Box],
 ['Bills','/admin/mobile/transactions',FileText],
 ['Staff','/admin/mobile/staff',Users],
 ['Reports','/admin/mobile/reports',BarChart3],
] as const;

export default function Layout({children,mobile=false}:{children:ReactNode;mobile?:boolean}){
 const[open,setOpen]=useState(false);const loc=useLocation();
 if(mobile){
  const moreActive=['/admin/mobile/returns','/admin/mobile/suppliers'].includes(loc.pathname);
  return <div className="mobile-stage">
   <div className="mobile-device-toolbar"><span>📱 Mobile Admin <small>/admin/mobile</small></span><span className="mobile-toolbar-badge">Mobile layout</span></div>
   <div className="mobile-device">
    <div className="mobile-status"><span>9:41</span><span className="mobile-notch"/><span>5G&nbsp; 100%</span></div>
    <header className="mobile-topbar">
     <div><b>THREAD<span>POS</span></b><small>Mobile Admin Hub</small></div>
     <button className="mobile-refresh" onClick={()=>window.location.reload()} aria-label="Refresh">↻</button>
    </header>
    <main className="mobile-page">{children}</main>
    <nav className="mobile-bottom-nav">
     {mobileLinks.map(([name,path,I])=><Link key={path} className={loc.pathname===path?'mobile-nav-item active':'mobile-nav-item'} to={path}><I size={19}/><span>{name}</span></Link>)}
     <button className={moreActive?'mobile-nav-item active':'mobile-nav-item'} onClick={()=>setOpen(v=>!v)}><MoreHorizontal size={19}/><span>More</span></button>
    </nav>
    {open&&<>
      <button className="mobile-sheet-backdrop" onClick={()=>setOpen(false)} aria-label="Close menu"/>
      <section className="mobile-more-sheet">
       <div className="mobile-sheet-handle"/><div className="mobile-sheet-title"><b>More Admin</b><button onClick={()=>setOpen(false)}>×</button></div>
       <Link to="/admin/mobile/returns" onClick={()=>setOpen(false)}><RotateCcw size={19}/>Product Returns</Link>
       <Link to="/admin/mobile/suppliers" onClick={()=>setOpen(false)}><Truck size={19}/>Suppliers & Purchases</Link>
       <Link to="/admin/mobile/transactions" onClick={()=>setOpen(false)}><FileText size={19}/>Billing Transactions</Link>
       <button onClick={logout}><LogOut size={19}/>Sign out</button>
      </section>
    </>}
   </div>
  </div>
 }
 const links=[['Dashboard','/admin',BarChart3],['Products','/admin/products',Box],['Staff','/admin/staff',Users],['Suppliers','/admin/suppliers',Truck],['Returns','/admin/returns',RotateCcw],['Billing & Transactions','/admin/transactions',FileText],['Ledger & Reports','/admin/reports',BarChart3]] as const;
 return <div className="shell">{open&&<button className="sidebar-backdrop" onClick={()=>setOpen(false)} aria-label="Close navigation"/>}<aside className={open?'sidebar open':'sidebar'}><div className="sidebar-head"><div className="brand">THREAD<span>POS</span></div><button className="sidebar-close" onClick={()=>setOpen(false)} aria-label="Close navigation"><X size={20}/></button></div><div className="side-title">ADMIN</div>{links.map(([n,p,I])=><Link onClick={()=>setOpen(false)} className={loc.pathname===p?'nav active':'nav'} to={p} key={p}><I size={18}/>{n}</Link>)}<button className="nav logout" onClick={logout}><LogOut size={18}/>Sign out</button></aside><div className="content"><header className="topbar"><button className="icon mobile-menu" onClick={()=>setOpen(!open)}>{open?<X/>:<Menu/>}</button><div><b>Admin Portal</b><small>{getUser()?.name}</small></div><Link className="top-billing" to="/billing"><ShoppingCart size={16}/>Billing</Link></header><main className="page">{children}</main></div></div>
}
