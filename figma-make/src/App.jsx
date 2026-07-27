import React, { useEffect, useMemo, useState } from "react";
import {
  BadgeCheck,
  BarChart3,
  Camera,
  CarFront,
  Check,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleDollarSign,
  Columns3,
  Fuel,
  Gauge,
  Heart,
  Languages,
  LayoutDashboard,
  List,
  MapPin,
  Menu,
  MessageSquare,
  Plus,
  Search,
  Share2,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  Upload,
  UserRound,
  WandSparkles,
  X,
} from "lucide-react";
import { filterOptions, vehicles } from "./data";

const money = (value) =>
  new Intl.NumberFormat("en-CA", {
    style: "currency",
    currency: "CAD",
    maximumFractionDigits: 0,
  }).format(value);

const km = (value) => `${new Intl.NumberFormat("en-CA").format(value)} km`;

function Brand() {
  return (
    <a className="brand" href="#" aria-label="AutoCommerce home">
      <span>AUTO</span>COMMERCE
    </a>
  );
}

function Header({ onSell }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  return (
    <header className="topbar">
      <Brand />
      <button
        className="icon-button mobile-menu"
        aria-label="Open navigation"
        onClick={() => setMobileOpen((value) => !value)}
      >
        {mobileOpen ? <X /> : <Menu />}
      </button>
      <nav className={mobileOpen ? "primary-nav open" : "primary-nav"}>
        <a className="active" href="#inventory">Buy</a>
        <button onClick={onSell}>Sell</button>
        <a href="#finance">Financing</a>
        <a href="#saved">Saved</a>
      </nav>
      <div className="header-actions">
        <button className="language"><Languages /> EN / FR</button>
        <button className="profile"><UserRound /> <span>My account</span></button>
        <button className="button secondary dashboard-button">
          <LayoutDashboard /> Seller dashboard
        </button>
      </div>
    </header>
  );
}

function SelectField({ label, value, onChange, children }) {
  return (
    <label className="field">
      <span>{label}</span>
      <div className="select-wrap">
        <select value={value} onChange={(event) => onChange(event.target.value)}>
          {children}
        </select>
        <ChevronDown aria-hidden="true" />
      </div>
    </label>
  );
}

function Filters({ filters, setFilters, onClose, resultCount }) {
  const reset = () =>
    setFilters({ make: "All makes", body: "All body types", fuel: "All fuel types", maxPrice: 50000 });
  return (
    <aside className="filters" aria-label="Vehicle filters">
      <div className="panel-heading">
        <div>
          <p className="section-label">Refine results</p>
          <h2>Filters</h2>
        </div>
        <button className="icon-button" onClick={onClose} aria-label="Close filters"><X /></button>
      </div>
      <button className="text-button" onClick={reset}>Clear all</button>

      <label className="field">
        <span>Location</span>
        <div className="input-with-icon">
          <MapPin />
          <input defaultValue="Toronto, ON" aria-label="Location" />
        </div>
      </label>
      <SelectField label="Make" value={filters.make} onChange={(make) => setFilters({ ...filters, make })}>
        {filterOptions.make.map((item) => <option key={item}>{item}</option>)}
      </SelectField>
      <SelectField label="Body type" value={filters.body} onChange={(body) => setFilters({ ...filters, body })}>
        {filterOptions.body.map((item) => <option key={item}>{item}</option>)}
      </SelectField>
      <SelectField label="Fuel type" value={filters.fuel} onChange={(fuel) => setFilters({ ...filters, fuel })}>
        {filterOptions.fuel.map((item) => <option key={item}>{item}</option>)}
      </SelectField>
      <label className="field range-field">
        <span>Maximum price <strong>{money(filters.maxPrice)}</strong></span>
        <input
          type="range"
          min="20000"
          max="50000"
          step="1000"
          value={filters.maxPrice}
          onChange={(event) => setFilters({ ...filters, maxPrice: Number(event.target.value) })}
        />
      </label>
      <div className="filter-spacer" />
      <button className="button primary full-width">Show {resultCount} vehicles</button>
      <button className="button ghost full-width"><Heart /> Save this search</button>
    </aside>
  );
}

function VehicleCard({ vehicle, selected, saved, onSelect, onSave, onCompare, compared }) {
  return (
    <article className={selected ? "vehicle-card selected" : "vehicle-card"}>
      <button className="card-main" onClick={() => onSelect(vehicle)} aria-label={`View ${vehicle.year} ${vehicle.make} ${vehicle.model}`}>
        <div className="vehicle-photo">
          <img src={vehicle.image} alt={`${vehicle.make} ${vehicle.model}`} />
          {vehicle.verified && <span className="verified-chip"><BadgeCheck /> VIN verified</span>}
        </div>
        <div className="vehicle-copy">
          <div className="vehicle-title-row">
            <div>
              <h3>{vehicle.year} {vehicle.make} {vehicle.model}</h3>
              <p>{vehicle.trim}</p>
            </div>
            <div className="price">
              <strong>{money(vehicle.price)}</strong>
              <span>{money(vehicle.monthly)}/mo*</span>
            </div>
          </div>
          <div className="vehicle-meta">
            <span><Gauge /> {km(vehicle.mileage)}</span>
            <span><MapPin /> {vehicle.location}</span>
          </div>
        </div>
      </button>
      <button className={saved ? "save-button saved" : "save-button"} onClick={() => onSave(vehicle.id)} aria-label="Save vehicle">
        <Heart fill={saved ? "currentColor" : "none"} />
      </button>
      <button className={compared ? "compare-button active" : "compare-button"} onClick={() => onCompare(vehicle)}>
        <Columns3 /> {compared ? "Added" : "Compare"}
      </button>
    </article>
  );
}

function VehicleDetail({ vehicle, onClose, onCompare, compared }) {
  const [activeImage, setActiveImage] = useState(0);
  const [descriptionOpen, setDescriptionOpen] = useState(false);
  const [messageSent, setMessageSent] = useState(false);
  useEffect(() => {
    setActiveImage(0);
    setDescriptionOpen(false);
    setMessageSent(false);
  }, [vehicle?.id]);
  if (!vehicle) return null;
  const gallery = [vehicle.image, vehicle.image, vehicle.image, vehicle.image, vehicle.image];
  const options = [
    "Air conditioning", "Alloy wheels", "Backup camera", "Bluetooth",
    "Brake assist", "Cruise control", "Heated seats", "Keyless entry",
    "Lane keeping assist", "Parking sensors", "Power seats", "Power windows",
    "Remote start", "Satellite radio", "Smartphone integration", "Wi-Fi hotspot",
  ];
  const details = [
    ["Make", vehicle.make],
    ["Model", vehicle.model],
    ["Trim", vehicle.trim],
    ["Year", vehicle.year],
    ["Exterior colour", vehicle.colour],
    ["Doors", vehicle.body === "Truck" ? "4" : "5"],
    ["Passengers", "5"],
    ["Transmission", vehicle.transmission],
    ["Engine", vehicle.fuel === "Electric" ? "Dual electric motor" : "2.0L 4-cylinder"],
    ["Fuel type", vehicle.fuel],
    ["VIN", vehicle.vin],
    ["Stock number", `AC-${vehicle.year}-${String(vehicle.id).padStart(4, "0")}`],
  ];
  return (
    <aside className="detail-panel">
      <div className="panel-heading detail-heading">
        <div>
          <p className="section-label">Quick view</p>
          <h2>{vehicle.year} {vehicle.make} {vehicle.model}</h2>
        </div>
        <button className="icon-button" onClick={onClose} aria-label="Close quick view"><X /></button>
      </div>
      <div className="detail-scroll">
        <section className="detail-gallery" aria-label="Vehicle photo gallery">
          <img className="detail-image" src={gallery[activeImage]} alt={`${vehicle.make} ${vehicle.model}, view ${activeImage + 1}`} />
          <div className="gallery-counter">{activeImage + 1}/{gallery.length}</div>
          <button className="gallery-next" onClick={() => setActiveImage((value) => (value + 1) % gallery.length)} aria-label="Next vehicle photo"><ChevronRight /></button>
          <div className="gallery-thumbnails">
            {gallery.map((image, index) => (
              <button className={activeImage === index ? "active" : ""} key={index} onClick={() => setActiveImage(index)} aria-label={`View photo ${index + 1}`}>
                <img src={image} alt="" />
              </button>
            ))}
          </div>
        </section>
        <div className="detail-body">
        {vehicle.verified && <div className="verification"><ShieldCheck /> VIN verified and decoded</div>}
        <div className="detail-price">
          <div>
            <span className="market-value">Competitive market price</span>
            <strong>{money(vehicle.price)}</strong>
          </div>
          <span>{money(vehicle.monthly)}/mo*</span>
        </div>
        <div className="detail-actions-row">
          <button className="icon-button" aria-label="Share vehicle"><Share2 /></button>
          <button className="icon-button" aria-label="Save vehicle"><Heart /></button>
        </div>
        <button className="button primary full-width"><MessageSquare /> Contact seller</button>
        <button className="button secondary full-width"><CircleDollarSign /> Request financing</button>

        <section className="detail-section">
          <h3>Overview</h3>
          <dl className="overview-grid">
            <div><dt><Gauge /> Mileage</dt><dd>{km(vehicle.mileage)}</dd></div>
            <div><dt><ShieldCheck /> Condition</dt><dd>{vehicle.year >= 2023 ? "New" : "Used"}</dd></div>
            <div><dt><CarFront /> Body</dt><dd>{vehicle.body}</dd></div>
            <div><dt><Fuel /> Fuel</dt><dd>{vehicle.fuel}</dd></div>
            <div><dt>Engine</dt><dd>{vehicle.fuel === "Electric" ? "Dual motor" : "2.0L 4-cylinder"}</dd></div>
            <div><dt>Passengers</dt><dd>5</dd></div>
            <div><dt>Transmission</dt><dd>{vehicle.transmission}</dd></div>
            <div><dt>Stock</dt><dd>AC-{vehicle.year}-{String(vehicle.id).padStart(4, "0")}</dd></div>
          </dl>
        </section>

        <section className="detail-section">
          <h3>Description</h3>
          <p className={descriptionOpen ? "vehicle-description open" : "vehicle-description"}>
            Discover this carefully selected {vehicle.year} {vehicle.make} {vehicle.model} {vehicle.trim}.
            It combines everyday comfort, confident performance and the practical equipment expected by Canadian drivers.
            The vehicle information has been structured from its VIN and reviewed before publication.
          </p>
          <button className="text-button read-more" onClick={() => setDescriptionOpen((value) => !value)}>
            {descriptionOpen ? "Read less" : "Read more"} <ChevronDown />
          </button>
        </section>

        <section className="detail-section">
          <h3>Options</h3>
          <ul className="option-grid">
            {options.map((option) => <li key={option}><Check /> {option}</li>)}
          </ul>
        </section>

        <section className="dealer-contact detail-section">
          <div className="section-title-row">
            <h3>Contact the dealer</h3>
            <a href="tel:+14165550198">+1 416-555-0198</a>
          </div>
          <div className="dealer-card">
            <strong>AutoGallery {vehicle.location.split(",")[0]}</strong>
            <span>{vehicle.location}</span>
            {messageSent ? (
              <div className="message-success"><Check /> Message sent. The dealer will contact you shortly.</div>
            ) : (
              <form onSubmit={(event) => { event.preventDefault(); setMessageSent(true); }}>
                <div className="form-row">
                  <label><span>First name</span><input required placeholder="First name" /></label>
                  <label><span>Last name</span><input required placeholder="Last name" /></label>
                </div>
                <label><span>Email address</span><input required type="email" placeholder="Email address" /></label>
                <label><span>Phone number</span><input type="tel" placeholder="Phone number (optional)" /></label>
                <label><span>Comment</span><textarea defaultValue={`Hello, I am interested in this ${vehicle.year} ${vehicle.make} ${vehicle.model}. Is it still available?`} /></label>
                <label className="trade-check"><input type="checkbox" /> I have a vehicle to trade</label>
                <button className="button primary full-width" type="submit">Send message</button>
              </form>
            )}
          </div>
        </section>

        <section className="detail-section">
          <h3>Vehicle details</h3>
          <dl className="detail-table">
            {details.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
          </dl>
        </section>

        <section className="detail-section">
          <h3>Technical characteristics</h3>
          <dl className="detail-table">
            <div><dt>Front suspension</dt><dd>MacPherson strut</dd></div>
            <div><dt>Rear suspension</dt><dd>Multi-link</dd></div>
            <div><dt>Drivetrain</dt><dd>{vehicle.trim.includes("AWD") || vehicle.trim.includes("xDrive") ? "All-wheel drive" : "Front-wheel drive"}</dd></div>
          </dl>
        </section>

        <section className="detail-section dealer-info">
          <h3>Dealer information</h3>
          <strong>AutoGallery {vehicle.location.split(",")[0]}</strong>
          <a href="tel:+14165550198">+1 416-555-0198</a>
          <span><MapPin /> {vehicle.location}</span>
          <button className="button secondary full-width">View all dealer listings</button>
        </section>

        <button className={compared ? "button ghost full-width active" : "button ghost full-width"} onClick={() => onCompare(vehicle)}>
          <Columns3 /> {compared ? "Remove from comparison" : "Add to comparison"}
        </button>
        <p className="detail-disclaimer">Prices exclude taxes, registration and applicable fees. Verify all vehicle information directly with the seller.</p>
        </div>
      </div>
    </aside>
  );
}

function CompareBar({ items, onRemove, onClear }) {
  if (!items.length) return null;
  return (
    <div className="compare-bar">
      <div className="compare-title"><Columns3 /><strong>Compare</strong><span>{items.length}/3</span></div>
      <div className="compare-items">
        {items.map((item) => (
          <div className="compare-item" key={item.id}>
            <img src={item.image} alt="" />
            <span>{item.year} {item.make} {item.model}</span>
            <button onClick={() => onRemove(item.id)} aria-label="Remove comparison"><X /></button>
          </div>
        ))}
        {items.length < 3 && <div className="compare-empty"><Plus /> Add vehicle</div>}
      </div>
      <button className="text-button" onClick={onClear}>Clear all</button>
      <button className="button primary" disabled={items.length < 2}>Compare now</button>
    </div>
  );
}

function SellModal({ onClose }) {
  const [step, setStep] = useState(1);
  const [vinValue, setVinValue] = useState("");
  const [generated, setGenerated] = useState(false);
  return (
    <div className="modal-backdrop" role="presentation" onMouseDown={onClose}>
      <section className="sell-modal" role="dialog" aria-modal="true" aria-labelledby="sell-title" onMouseDown={(event) => event.stopPropagation()}>
        <div className="modal-header">
          <div>
            <p className="section-label">Smart listing studio</p>
            <h2 id="sell-title">Sell your vehicle</h2>
          </div>
          <button className="icon-button" onClick={onClose}><X /></button>
        </div>
        <div className="steps">
          {["Decode VIN", "Add photos", "Generate listing"].map((label, index) => (
            <div className={step >= index + 1 ? "step active" : "step"} key={label}>
              <span>{index + 1}</span>{label}
            </div>
          ))}
        </div>
        {step === 1 && (
          <div className="modal-content">
            <div className="feature-icon"><BadgeCheck /></div>
            <h3>Start with the VIN</h3>
            <p>AutoCommerce decodes the technical details so you do not have to enter them manually.</p>
            <label className="field">
              <span>17-character VIN</span>
              <input placeholder="Example: 2HKRW2H85NH201234" value={vinValue} onChange={(event) => setVinValue(event.target.value.toUpperCase())} maxLength={17} />
            </label>
            <button className="button primary full-width" disabled={vinValue.length < 8} onClick={() => setStep(2)}>
              <Sparkles /> Decode vehicle
            </button>
          </div>
        )}
        {step === 2 && (
          <div className="modal-content">
            <div className="decoded-banner"><ShieldCheck /> 2022 Honda CR-V EX-L AWD identified</div>
            <button className="upload-zone" onClick={() => setStep(3)}>
              <Camera />
              <strong>Upload vehicle photos</strong>
              <span>Drag and drop or select up to 24 images</span>
              <small>AI quality check, blur detection and smart ordering included</small>
            </button>
            <button className="button secondary full-width" onClick={() => setStep(3)}><Upload /> Use demo photos</button>
          </div>
        )}
        {step === 3 && (
          <div className="modal-content">
            <div className="ai-summary">
              <WandSparkles />
              <div>
                <strong>AI Listing Assistant</strong>
                <p>Vehicle data and 12 photos are ready. Generate a transparent, factual description in seconds.</p>
              </div>
            </div>
            {!generated ? (
              <button className="button primary full-width" onClick={() => setGenerated(true)}><Sparkles /> Generate listing</button>
            ) : (
              <>
                <div className="generated-copy">
                  <strong>2022 Honda CR-V EX-L AWD — one-owner, versatile and refined</strong>
                  <p>Well-equipped Canadian SUV with leather interior, all-wheel drive, heated seats and advanced safety technology. VIN details verified by AutoCommerce.</p>
                </div>
                <button className="button primary full-width" onClick={onClose}>Publish listing</button>
              </>
            )}
          </div>
        )}
      </section>
    </div>
  );
}

export default function App() {
  const [filtersOpen, setFiltersOpen] = useState(true);
  const [detail, setDetail] = useState(vehicles[0]);
  const [saved, setSaved] = useState([1]);
  const [compared, setCompared] = useState([vehicles[0], vehicles[1]]);
  const [view, setView] = useState("grid");
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("recommended");
  const [sellOpen, setSellOpen] = useState(false);
  const [filters, setFilters] = useState({
    make: "All makes",
    body: "All body types",
    fuel: "All fuel types",
    maxPrice: 50000,
  });

  const results = useMemo(() => {
    const normalized = query.toLowerCase();
    const filtered = vehicles.filter((vehicle) => {
      const matchesQuery = `${vehicle.year} ${vehicle.make} ${vehicle.model} ${vehicle.trim}`.toLowerCase().includes(normalized);
      return (
        matchesQuery &&
        (filters.make === "All makes" || vehicle.make === filters.make) &&
        (filters.body === "All body types" || vehicle.body === filters.body) &&
        (filters.fuel === "All fuel types" || vehicle.fuel === filters.fuel) &&
        vehicle.price <= filters.maxPrice
      );
    });
    return [...filtered].sort((a, b) => {
      if (sort === "price-low") return a.price - b.price;
      if (sort === "price-high") return b.price - a.price;
      if (sort === "mileage") return a.mileage - b.mileage;
      return b.year - a.year;
    });
  }, [filters, query, sort]);

  const toggleSave = (id) =>
    setSaved((items) => items.includes(id) ? items.filter((item) => item !== id) : [...items, id]);

  const toggleCompare = (vehicle) =>
    setCompared((items) => {
      if (items.some((item) => item.id === vehicle.id)) return items.filter((item) => item.id !== vehicle.id);
      return items.length < 3 ? [...items, vehicle] : items;
    });

  return (
    <div className="app-shell">
      <Header onSell={() => setSellOpen(true)} />
      <main className={`marketplace ${filtersOpen ? "with-filters" : ""} ${detail ? "with-detail" : ""}`}>
        {filtersOpen && (
          <Filters
            filters={filters}
            setFilters={setFilters}
            onClose={() => setFiltersOpen(false)}
            resultCount={results.length}
          />
        )}
        <section className="inventory" id="inventory">
          <div className="inventory-header">
            <div>
              <p className="section-label">Canadian marketplace</p>
              <h1>Find your next vehicle</h1>
              <p className="result-count">{results.length} curated vehicles near you</p>
            </div>
            <button className="button secondary" onClick={() => setSellOpen(true)}><Plus /> Sell your vehicle</button>
          </div>
          <div className="inventory-toolbar">
            {!filtersOpen && <button className="button filter-toggle" onClick={() => setFiltersOpen(true)}><SlidersHorizontal /> Filters</button>}
            <label className="search-box">
              <Search />
              <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search make, model or keyword" aria-label="Search inventory" />
              {query && <button onClick={() => setQuery("")} aria-label="Clear search"><X /></button>}
            </label>
            <label className="sort-box">
              <span>Sort</span>
              <select value={sort} onChange={(event) => setSort(event.target.value)}>
                <option value="recommended">Recommended</option>
                <option value="price-low">Price: low to high</option>
                <option value="price-high">Price: high to low</option>
                <option value="mileage">Lowest mileage</option>
              </select>
            </label>
            <div className="view-toggle" aria-label="View options">
              <button className={view === "grid" ? "active" : ""} onClick={() => setView("grid")} aria-label="Grid view"><BarChart3 /></button>
              <button className={view === "list" ? "active" : ""} onClick={() => setView("list")} aria-label="List view"><List /></button>
            </div>
          </div>
          {results.length ? (
            <div className={`vehicle-grid ${view}`}>
              {results.map((vehicle) => (
                <VehicleCard
                  key={vehicle.id}
                  vehicle={vehicle}
                  selected={detail?.id === vehicle.id}
                  saved={saved.includes(vehicle.id)}
                  compared={compared.some((item) => item.id === vehicle.id)}
                  onSelect={setDetail}
                  onSave={toggleSave}
                  onCompare={toggleCompare}
                />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <Search />
              <h2>No vehicles match these filters</h2>
              <p>Try widening your price range or clearing one of the filters.</p>
              <button className="button primary" onClick={() => {
                setQuery("");
                setFilters({ make: "All makes", body: "All body types", fuel: "All fuel types", maxPrice: 50000 });
              }}>Reset search</button>
            </div>
          )}
          <nav className="pagination" aria-label="Pagination">
            <button aria-label="Previous page"><ChevronLeft /></button>
            <button className="active">1</button>
            <button>2</button>
            <button>3</button>
            <span>…</span>
            <button>703</button>
            <button aria-label="Next page"><ChevronRight /></button>
          </nav>
        </section>
        <VehicleDetail
          vehicle={detail}
          onClose={() => setDetail(null)}
          onCompare={toggleCompare}
          compared={compared.some((item) => item.id === detail?.id)}
        />
      </main>
      <CompareBar
        items={compared}
        onRemove={(id) => setCompared((items) => items.filter((item) => item.id !== id))}
        onClear={() => setCompared([])}
      />
      {!detail && <button className="floating-detail" onClick={() => setDetail(vehicles[0])}><CarFront /> Quick view</button>}
      {sellOpen && <SellModal onClose={() => setSellOpen(false)} />}
    </div>
  );
}
