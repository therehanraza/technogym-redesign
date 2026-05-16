import React, { StrictMode, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  Heart,
  Menu,
  Search,
  ShoppingBag,
  Trash2,
  User,
  X,
} from "lucide-react";
import { api } from "./api";
import { fallbackCategories, fallbackProducts } from "./data";
import "./styles.css";

const pageMap = {
  "/shop": ["Shop Home Essentials", "Curated premium products for modern home wellness.", "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=1400&q=85"],
  "/home-gym": ["Home Gym Design", "Create a personal training room with premium equipment, layout support and connected workouts.", "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85"],
  "/business": ["Commercial Gym Machines and Pro Equipment", "Solutions for clubs, hotels, corporate wellness, medical and sports facilities.", "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85"],
  "/support": ["Support", "Customer support, technical assistance, e-learning and service flows.", "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=1400&q=85"],
  "/contacts": ["Contact Us", "Lead form and contact flow for consultation, marketing and technical requests.", "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?auto=format&fit=crop&w=1400&q=85"],
  "/checkout": ["Checkout", "Modern ecommerce checkout for selected products and consultation-led purchasing.", "https://images.unsplash.com/photo-1556742502-ec7c0e9f34b1?auto=format&fit=crop&w=1400&q=85"],
  "/design": ["Design at Technogym", "Interior design, premium materials, layouts and design-led wellness experiences.", "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85"],
  "/room-planner": ["Room Planner", "Create room layouts, add equipment and build your gym concept.", "https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85"],
  "/stories": ["Stories", "Editorial hub for longevity, people, sports, fitness, health, mind and nutrition.", "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=1400&q=85"],
  "/account": ["My Account", "Profile, orders, saved consultations and app-connected preferences.", "https://images.unsplash.com/photo-1556745757-8d76bdb6984b?auto=format&fit=crop&w=1400&q=85"],
};

const businessCards = [
  ["Health Clubs", "/business/health-clubs", "Premium fitness club layouts, cardio lines and strength zones.", "https://images.unsplash.com/photo-1534258936925-c58bed479fcb?auto=format&fit=crop&w=900&q=85"],
  ["Hospitality", "/business/hospitality", "Hotel wellness rooms and resort fitness experiences.", "https://images.unsplash.com/photo-1571902943202-507ec2618e8f?auto=format&fit=crop&w=900&q=85"],
  ["Corporate", "/business/corporate", "Employee wellness spaces for productive workplaces.", "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=900&q=85"],
  ["Medical", "/business/medical", "Rehabilitation and active ageing movement environments.", "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=85"],
];

const megaMenus = {
  products: {
    eyebrow: "Products",
    title: "Explore Products",
    text: "All links are routed inside this redesigned frontend.",
    columns: [
      ["All Products", "/category/all-products"],
      ["Shop Home Essentials", "/shop"],
      ["Treadmills", "/category/treadmills"],
      ["Bikes", "/category/exercise-bikes"],
      ["Ellipticals", "/category/ellipticals"],
      ["Rower", "/category/rower"],
      ["Stair Climbers", "/category/stair-climbers"],
      ["Multi Gyms", "/category/multi-gyms"],
      ["Dumbbells & Kettlebells", "/category/free-weights"],
      ["Benches", "/category/benches"],
      ["Barbells & Plates", "/category/free-weights"],
      ["Racks", "/category/multi-gyms"],
    ],
  },
  home: {
    eyebrow: "Home Gym",
    title: "Explore Home Gym",
    text: "All links are routed inside this redesigned frontend.",
    columns: [
      ["Home Gym", "/home-gym"],
      ["Luxury Home Gym", "/luxury-home-gym"],
      ["Lifestyle Home Gym", "/lifestyle-home-gym"],
      ["Room Planner", "/room-planner"],
      ["Design at Technogym", "/design"],
    ],
  },
  business: {
    eyebrow: "Business",
    title: "Explore Business",
    text: "All links are routed inside this redesigned frontend.",
    columns: [
      ["Business", "/business"],
      ["Commercial Equipment", "/business-equipment"],
      ["Fitness Clubs", "/business/health-clubs"],
      ["Hotels & Resorts", "/business/hospitality"],
      ["Corporate Wellness", "/business/corporate"],
      ["Medical & Rehab", "/business/medical"],
    ],
  },
  support: {
    eyebrow: "Support",
    title: "Explore Support",
    text: "All links are routed inside this redesigned frontend.",
    columns: [
      ["Support Home", "/support"],
      ["Technogym Care", "/technogym-care"],
      ["Technical Support", "/technical-support"],
      ["Contacts", "/contacts"],
      ["Technogym App", "/technogym-app"],
    ],
  },
  stories: {
    eyebrow: "Stories",
    title: "Explore Stories",
    text: "All links are routed inside this redesigned frontend.",
    columns: [
      ["Stories", "/stories"],
      ["Wellness", "/wellness"],
      ["Sustainability", "/sustainability"],
      ["Design", "/design"],
    ],
  },
};

function getPath() {
  return window.location.hash.replace("#", "") || "/";
}

function Link({ to, children, className = "", onClick }) {
  return (
    <a href={`#${to}`} className={className} onClick={onClick}>
      {children}
    </a>
  );
}

function Header({ cartCount, onSearch, onCart }) {
  const [open, setOpen] = useState(false);
  const [activeMenu, setActiveMenu] = useState(null);
  const links = [
    ["Products", "/category/all-products", "products"],
    ["Home Gym", "/home-gym", "home"],
    ["Business", "/business", "business"],
    ["Support", "/support", "support"],
    ["Stories", "/stories", "stories"],
  ];
  return (
    <div className="nav-system">
      <header className="site-header">
        <Link to="/" className="brand" onClick={() => setActiveMenu(null)}>TECHNOGYM</Link>
        <nav className="desktop-nav">
          {links.map(([label, , menuKey]) => (
            <button
              key={label}
              type="button"
              className={`nav-link ${activeMenu === menuKey ? "active" : ""}`}
              onClick={() => setActiveMenu((current) => current === menuKey ? null : menuKey)}
              onFocus={() => setActiveMenu(menuKey)}
              onMouseEnter={() => setActiveMenu(menuKey)}
            >
              {label}<ChevronDown size={14} />
            </button>
          ))}
        </nav>
        <div className="header-actions">
          <button aria-label="Search" className="icon-button" onClick={onSearch}><Search /></button>
          <Link to="/account" className="icon-button" aria-label="Account"><User /></Link>
          <button aria-label="Cart" className="icon-button cart-button" onClick={onCart}><ShoppingBag /><span>{cartCount}</span></button>
          <Link to="/contacts" className="primary-pill">Book Consultation</Link>
          <button aria-label="Menu" className="icon-button mobile-only" onClick={() => setOpen(true)}><Menu /></button>
        </div>
        {open && (
          <div className="mobile-menu">
            <button className="icon-button close" onClick={() => setOpen(false)}><X /></button>
            {links.map(([label, to]) => <Link key={label} to={to} onClick={() => setOpen(false)}>{label}</Link>)}
            <Link to="/contacts" className="primary-pill mobile-cta" onClick={() => setOpen(false)}>Book Consultation</Link>
          </div>
        )}
      </header>
      {activeMenu && (
        <div
          className="mega-menu"
          onMouseEnter={() => setActiveMenu(activeMenu)}
        >
          <div className="mega-inner container">
            <div className="mega-copy">
              <p className="eyebrow">{megaMenus[activeMenu].eyebrow}</p>
              <h2>{megaMenus[activeMenu].title}</h2>
              <p>{megaMenus[activeMenu].text}</p>
            </div>
            <div className="mega-grid">
              {megaMenus[activeMenu].columns.map(([label, to]) => (
                <Link key={`${activeMenu}-${label}`} to={to} className="mega-card" onClick={() => setActiveMenu(null)}>
                  {label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Hero() {
  return (
    <section className="hero">
      <div className="hero-grid container">
        <div>
          <p className="eyebrow chip">Premium wellness equipment redesigned for modern India</p>
          <h1>A complete modern redesign for Technogym experience.</h1>
          <p className="hero-copy">Home gym, commercial gym, products, support, stories and consultation flows redesigned in one complete full-stack website.</p>
          <div className="hero-actions">
            <Link to="/shop" className="primary-cta">Shop now <ArrowRight size={18} /></Link>
            <Link to="/business" className="secondary-cta">Business solutions</Link>
          </div>
          <div className="stats">
            <span><b>14+</b> Categories</span><span><b>12</b> Product pages</span><span><b>100%</b> Functional forms</span>
          </div>
        </div>
        <div className="hero-media">
          <img src="https://images.unsplash.com/photo-1605296867304-46d5465a13f1?auto=format&fit=crop&w=1400&q=85" alt="Luxury home gym" />
          <div className="caption"><small>Featured</small><b>Luxury Home Gym Setup</b></div>
        </div>
      </div>
    </section>
  );
}

function ProductCard({ product, onAdd }) {
  return (
    <article className="product-card">
      <Link to={`/product/${product.slug}`} className="product-image">
        <img src={product.image} alt={product.name} />
        <span>{product.tag || "Featured"}</span>
      </Link>
      <div className="product-body">
        <p>{product.category}</p>
        <div className="product-title"><h3>{product.name}</h3><Heart size={18} /></div>
        <p className="muted">{product.description}</p>
        <div className="product-footer"><b>{product.price}</b><button onClick={() => onAdd(product)}>Add</button></div>
      </div>
    </article>
  );
}

function Home({ categories, products, onAdd }) {
  return (
    <>
      <Hero />
      <section className="section container">
        <div className="section-head"><div><p className="eyebrow">Shop by category</p><h2>Every equipment category covered</h2></div><Link to="/category/all-products">View all categories</Link></div>
        <div className="category-grid">
          {categories.slice(0, 8).map((item) => <Link key={item.slug} to={`/category/${item.slug}`} className="category-card"><img src={item.image} alt="" /><h3>{item.name}</h3><p>{item.description}</p></Link>)}
        </div>
      </section>
      <section className="section dark-band">
        <div className="container">
          <div className="center-head"><p className="eyebrow">Featured Products</p><h2>Premium product showcase</h2></div>
          <div className="product-grid">{products.slice(0, 8).map((product) => <ProductCard key={product.slug} product={product} onAdd={onAdd} />)}</div>
        </div>
      </section>
      <section className="section container">
        <div className="section-head"><div><p className="eyebrow">Business</p><h2>Commercial solutions</h2></div></div>
        <div className="business-grid">{businessCards.map(([name, path, text, image]) => <Link key={name} to={path} className="category-card"><img src={image} alt="" /><h3>{name}</h3><p>{text}</p></Link>)}</div>
      </section>
      <section className="design-band">
        <div className="container design-grid">
          <img src="https://images.unsplash.com/photo-1558611848-73f7eb4001a1?auto=format&fit=crop&w=1400&q=85" alt="Gym room design" />
          <div><p className="eyebrow dark">Design & room planner</p><h2>Plan a premium gym before buying equipment.</h2><p>Room planner, interior design, layout consultation and curated product selection.</p><Link to="/room-planner" className="dark-button">Open Room Planner</Link></div>
        </div>
      </section>
    </>
  );
}

function Listing({ slug, categories, products, onAdd }) {
  const selected = categories.find((item) => item.slug === slug);
  const shown = selected ? products.filter((product) => product.category.toLowerCase().includes(selected.name.split(" ")[0].toLowerCase())) : products;
  return (
    <>
      <PageHero title={selected?.name || "All exercise equipment"} eyebrow="Products" text={selected?.description || "Explore cardio, strength, accessories, room planning and commercial equipment in one redesigned listing."} image={selected?.image || categories[0]?.image} />
      <section className="listing container">
        <aside className="filter-panel"><h3>Categories</h3><Link to="/category/all-products">All Products</Link>{categories.map((item) => <Link key={item.slug} to={`/category/${item.slug}`}>{item.name}</Link>)}</aside>
        <main><div className="listing-meta"><p>{shown.length || products.length} products shown</p><select><option>Sort: Featured</option><option>Price: Low to High</option><option>Newest</option></select></div><div className="product-grid three">{(shown.length ? shown : products).map((product) => <ProductCard key={product.slug} product={product} onAdd={onAdd} />)}</div></main>
      </section>
    </>
  );
}

function ProductDetail({ slug, products, onAdd }) {
  const product = products.find((item) => item.slug === slug) || products[0];
  const related = products.filter((item) => item.slug !== product.slug).slice(0, 3);
  return (
    <>
      <section className="detail container">
        <div><img className="detail-image" src={product.image} alt={product.name} /><div className="thumb-row"><img src={product.image} alt="" /><img src={product.image} alt="" /><img src={product.image} alt="" /></div></div>
        <div className="detail-copy"><p className="eyebrow">{product.category}</p><h1>{product.name}</h1><p>{product.description}</p><b>{product.price}</b><div className="hero-actions"><button className="primary-cta" onClick={() => onAdd(product)}>Add to Cart</button><Link to="/contacts" className="secondary-cta">Request Quote</Link></div><div className="specs">{(product.specs || []).map((spec) => <span key={spec}><CheckCircle2 />{spec}</span>)}</div></div>
      </section>
      <section className="section dark-band"><div className="container"><h2>Related products</h2><div className="product-grid three">{related.map((item) => <ProductCard key={item.slug} product={item} onAdd={onAdd} />)}</div></div></section>
    </>
  );
}

function PageHero({ eyebrow, title, text, image }) {
  return <section className="page-hero"><div className="container page-grid"><div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{text}</p></div>{image && <img src={image} alt="" />}</div></section>;
}

function RequestForm({ mode, cart, onOrderComplete }) {
  const [form, setForm] = useState({ fullName: "", emailOrPhone: "", requirementType: "Home Gym", message: "", address: "" });
  const [status, setStatus] = useState({ loading: false, message: "", error: "" });
  const isCheckout = mode === "checkout";

  const update = (event) => setForm((value) => ({ ...value, [event.target.name]: event.target.value }));
  const validate = () => {
    if (form.fullName.trim().length < 2) return "Please enter your full name.";
    if (form.emailOrPhone.trim().length < 5) return "Please enter a valid email or phone number.";
    if (isCheckout && cart.length === 0) return "Your cart is empty. Add a product before checkout.";
    return "";
  };
  const submit = async (event) => {
    event.preventDefault();
    const error = validate();
    if (error) return setStatus({ loading: false, message: "", error });
    setStatus({ loading: true, message: "", error: "" });
    try {
      if (isCheckout) {
        await api.createOrder({ customer: { fullName: form.fullName, emailOrPhone: form.emailOrPhone, address: form.address }, items: cart.map((item) => ({ name: item.name, slug: item.slug, price: item.price, quantity: 1 })), notes: form.message });
        onOrderComplete();
      } else {
        await api.createInquiry({ fullName: form.fullName, emailOrPhone: form.emailOrPhone, requirementType: form.requirementType, message: form.message });
      }
      setForm({ fullName: "", emailOrPhone: "", requirementType: "Home Gym", message: "", address: "" });
      setStatus({ loading: false, message: isCheckout ? "Order request created. Our team will confirm availability soon." : "Your consultation request was submitted successfully.", error: "" });
    } catch (err) {
      setStatus({ loading: false, message: "", error: err.message });
    }
  };
  return (
    <form className="request-form" onSubmit={submit}>
      <input name="fullName" value={form.fullName} onChange={update} placeholder="Full Name" />
      <input name="emailOrPhone" value={form.emailOrPhone} onChange={update} placeholder="Email / Phone" />
      <select name="requirementType" value={form.requirementType} onChange={update}><option>Home Gym</option><option>Commercial</option><option>Support</option><option>Design Consultation</option></select>
      {isCheckout && <input name="address" value={form.address} onChange={update} placeholder="Delivery address" />}
      <textarea name="message" value={form.message} onChange={update} placeholder="Requirement details" />
      {status.error && <p className="form-error">{status.error}</p>}
      {status.message && <p className="form-success">{status.message}</p>}
      <button className="primary-cta" disabled={status.loading}>{status.loading ? "Submitting..." : isCheckout ? "Place Request" : "Submit"}</button>
    </form>
  );
}

function GenericPage({ path, cart, onOrderComplete }) {
  const key = path.startsWith("/stories/") ? "/stories" : path;
  const data = pageMap[key] || ["Page Ready", "This route is handled inside the redesigned experience.", "https://images.unsplash.com/photo-1517963879433-6ad2b056d712?auto=format&fit=crop&w=1400&q=85"];
  const needsForm = key === "/contacts" || key === "/checkout";
  return (
    <>
      <PageHero eyebrow="Technogym Redesign" title={data[0]} text={data[1]} image={data[2]} />
      <section className="section container">
        {needsForm ? <div className="form-shell"><div><h2>{key === "/checkout" ? "Complete your request" : "Submit your request"}</h2><p>Connected to the Python backend with validation, loading state, and success/error feedback.</p></div><RequestForm mode={key === "/checkout" ? "checkout" : "inquiry"} cart={cart} onOrderComplete={onOrderComplete} /></div> : <div className="feature-grid">{["Premium UI", "Responsive Layout", "Clickable Flow"].map((item) => <div className="feature-card" key={item}><h3>{item}</h3><p>Designed as a complete portfolio-ready page, not a dead-end placeholder.</p></div>)}</div>}
      </section>
    </>
  );
}

function SearchOverlay({ open, onClose, products }) {
  const [query, setQuery] = useState("");
  const results = products.filter((item) => item.name.toLowerCase().includes(query.toLowerCase()) || item.category.toLowerCase().includes(query.toLowerCase())).slice(0, 5);
  if (!open) return null;
  return <div className="overlay"><div className="search-panel"><button className="icon-button close" onClick={onClose}><X /></button><input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search products, services, support" />{query && results.map((item) => <Link key={item.slug} to={`/product/${item.slug}`} onClick={onClose}>{item.name}<span>{item.category}</span></Link>)}</div></div>;
}

function CartDrawer({ open, onClose, cart, remove }) {
  if (!open) return null;
  return <div className="drawer-wrap"><div className="drawer"><button className="icon-button close" onClick={onClose}><X /></button><h2>Your selection</h2>{cart.length === 0 ? <p className="muted">No equipment added yet.</p> : cart.map((item, index) => <div className="cart-line" key={`${item.slug}-${index}`}><img src={item.image} alt="" /><div><b>{item.name}</b><p>{item.price}</p></div><button onClick={() => remove(index)}><Trash2 size={18} /></button></div>)}<Link to="/checkout" onClick={onClose} className="primary-cta wide">Continue to Checkout</Link></div></div>;
}

function App() {
  const [path, setPath] = useState(getPath());
  const [categories, setCategories] = useState(fallbackCategories);
  const [products, setProducts] = useState(fallbackProducts);
  const [searchOpen, setSearchOpen] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const sync = () => setPath(getPath());
    window.addEventListener("hashchange", sync);
    return () => window.removeEventListener("hashchange", sync);
  }, []);

  useEffect(() => {
    Promise.all([api.getCategories(), api.getProducts()])
      .then(([catRes, prodRes]) => {
        if (catRes?.data?.length) setCategories(catRes.data);
        if (prodRes?.data?.length) setProducts(prodRes.data);
      })
      .catch(() => {});
  }, []);

  const content = useMemo(() => {
    if (path === "/") return <Home categories={categories} products={products} onAdd={(item) => { setCart((current) => [...current, item]); setCartOpen(true); }} />;
    if (path === "/category/all-products") return <Listing categories={categories} products={products} onAdd={(item) => { setCart((current) => [...current, item]); setCartOpen(true); }} />;
    if (path.startsWith("/category/")) return <Listing slug={path.split("/").pop()} categories={categories} products={products} onAdd={(item) => { setCart((current) => [...current, item]); setCartOpen(true); }} />;
    if (path.startsWith("/product/")) return <ProductDetail slug={path.split("/").pop()} products={products} onAdd={(item) => { setCart((current) => [...current, item]); setCartOpen(true); }} />;
    return <GenericPage path={path} cart={cart} onOrderComplete={() => setCart([])} />;
  }, [path, categories, products, cart]);

  return (
    <>
      <Header cartCount={cart.length} onSearch={() => setSearchOpen(true)} onCart={() => setCartOpen(true)} />
      {content}
      <footer><div className="container footer-grid"><b>TECHNOGYM</b><p>Portfolio redesign of the original Technogym experience for modern full-stack presentation.</p><Link to="/contacts">Contact</Link></div></footer>
      <SearchOverlay open={searchOpen} onClose={() => setSearchOpen(false)} products={products} />
      <CartDrawer open={cartOpen} onClose={() => setCartOpen(false)} cart={cart} remove={(index) => setCart((items) => items.filter((_, itemIndex) => itemIndex !== index))} />
    </>
  );
}

createRoot(document.getElementById("root")).render(<StrictMode><App /></StrictMode>);
