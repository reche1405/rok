import os,  datetime
from promo.app import create_app  # Imports your Flask app instance
from promo.models import db  # Imports your SQLAlchemy instance
from promo.models.service import Service  # Adjust path to your actual Service model
from promo.models.project import Project, Unit  # Adjust path to your actual Project model
from promo.models.area import Area
from promo.models.location import Location
from promo.models.meta import Meta, Page
from promo.models.article import Article
from promo.models.social import Social
from promo.models.list import List, ListItem
from promo.models.policy import Policy


def seed_database():
    print("Initializing database seeding process with slug fields...")
    # 1. Complete dataset with custom URL slugs included
    
    
    services_data = [
        {
            "title": "Groundworks, Excavation & Concrete Structures",
            "slug": "groundworks-excavation-and-concrete-structures",
            "short_desc": "We engineer stable structural baselines, executing deep excavations and pouring reinforced foundations to eliminate future settlement risks.",
            "desc": (
                "Set the fundamental parameters of your structure with our high-intensity groundworks and concrete division. "
                "We execute deep topographical excavations, install complex subsurface drainage paths, construct robust earth-retaining walls, and pour steel-reinforced concrete ground beams. "
                "Our engineers focus entirely on geotechnically sound preparation to eliminate future settlement risks."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pickaxe-icon lucide-pickaxe"><path d="m14 13-8.381 8.38a1 1 0 0 1-3.001-3L11 9.999"/><path d="M15.973 4.027A13 13 0 0 0 5.902 2.373c-1.398.342-1.092 2.158.277 2.601a19.9 19.9 0 0 1 5.822 3.024"/><path d="M16.001 11.999a19.9 19.9 0 0 1 3.024 5.824c.444 1.369 2.26 1.676 2.603.278A13 13 0 0 0 20 8.069"/><path d="M18.352 3.352a1.205 1.205 0 0 0-1.704 0l-5.296 5.296a1.205 1.205 0 0 0 0 1.704l2.296 2.296a1.205 1.205 0 0 0 1.704 0l5.296-5.296a1.205 1.205 0 0 0 0-1.704z"/></svg>',
            "benefits_list": [
                "Provides an unyielding, geotechnically verified structural footprint.",
                "Diverts destructive surface stormwater safely away from foundations.",
                "Prevents dangerous structural shifting or uneven building settlement.",
                "Creates perfect structural datums for subsequent frame trades.",
                "Excellent sub-base preparation for roads, paths, and slabs."
            ]
        },
        {
            "title": "Structural Bricklaying & Architectural Stonemasonry",
            "slug": "structural-bricklaying-and-architectural-stonemasonry",
            "short_desc": "We build high-capacity load-bearing envelopes and hand-dress premium facades to secure the physical durability of your building asset.",
            "desc": (
                "Establish solid building parameters with our specialist bricklaying and structural masonry solutions. "
                "We construct load-bearing exterior brick envelopes, internal blockwork acoustic partitions, retaining earth walls, and elegant natural stone features. "
                "Our bricklayers focus heavily on meticulous alignment, structurally verified mortar mixes, and seamless historical pointing matching."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cuboid-icon lucide-cuboid"><path d="M10 22v-8"/><path d="M2.336 8.89 10 14l11.715-7.029"/><path d="M22 14a2 2 0 0 1-.971 1.715l-10 6a2 2 0 0 1-2.138-.05l-6-4A2 2 0 0 1 2 16v-6a2 2 0 0 1 .971-1.715l10-6a2 2 0 0 1 2.138.05l6 4A2 2 0 0 1 22 8z"/></svg>',
            "benefits_list": [
                "Maximum load-bearing capacities for multi-story additions.",
                "Outstanding built-in fire-resistance characteristics.",
                "Virtually zero long-term degradation or maintenance costs.",
                "Superior thermal mass attributes for climate regulation.",
                "Excellent acoustic dampening between adjacent spaces."
            ]
        },
        {
            "title": "Carpentry, Joinery & Structural Framing",
            "slug": "carpentry-joinery-and-structural-framing",
            "short_desc": "We erect precision structural timber frameworks, configure complex heavy formwork, and install bespoke millwork to optimize internal space layouts.",
            "desc": (
                "From structural skeletal frames to high-end architectural finishes, our carpentry services cover all timber requirements. "
                "We execute first-fix roofing frameworks, heavy concrete shuttering formwork, and precise window/door installations. "
                "Our joiners also craft premium second-fix details including skirting, bespoke fitted cabinetry, and high-end millwork pieces."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-fence-icon lucide-fence"><path d="M4 3 2 5v15c0 .6.4 1 1 1h2c.6 0 1-.4 1-1V5Z"/><path d="M6 8h4"/><path d="M6 18h4"/><path d="m12 3-2 2v15c0 .6.4 1 1 1h2c.6 0 1-.4 1-1V5Z"/><path d="M14 8h4"/><path d="M14 18h4"/><path d="m20 3-2 2v15c0 .6.4 1 1 1h2c.6 0 1-.4 1-1V5Z"/></svg>',
            "benefits_list": [
                "Structural precision for perfectly plumb walls and roofs.",
                "Bespoke, custom-tailored storage and design layout options.",
                "Utilizes premium timber species for lasting aesthetic beauty.",
                "Increases the luxurious feel and value of interior spaces.",
                "Seamless integration with electrical and plumbing access pathways."
            ]
        },
        {
            "title": "Roofing Systems & External Envelopes",
            "slug": "roofing-systems-and-external-envelopes",
            "short_desc": "We seal the entire building envelope against harsh elements, deploying multi-layer waterproofing barriers to eliminate water damage vectors.",
            "desc": (
                "Protect your asset from the elements with our comprehensive roofing and external envelope services. "
                "We specialize in full structural roof installations, localized leak repairs, tile replacements, flat-roof GRP systems, and advanced below-grade basement tanking. "
                "Our team deploys cutting-edge weather protection wrappers and liquid membranes to keep your entire asset completely dry."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-triangle-right-icon lucide-triangle-right"><path d="M22 18a2 2 0 0 1-2 2H3c-1.1 0-1.3-.6-.4-1.3L20.4 4.3c.9-.7 1.6-.4 1.6.7Z"/></svg>',
            "benefits_list": [
                "Guarantees total weatherproofing against harsh elements.",
                "Prevents expensive timber rot and internal structural damage.",
                "Improves roof insulation to lock in building heat.",
                "Prevents catastrophic basement flooding and damp ingress.",
                "Saves thousands in structural water damage restorations."
            ]
        },
        {
            "title": "Drywall, Partitioning & Advanced Insulation",
            "slug": "drywall-partitioning-and-advanced-insulation",
            "short_desc": "We isolate internal thermal and acoustic pathways, assembling specialized fire-rated partitions to maximize room-to-room containment.",
            "desc": (
                "Craft interior space plans with our high-speed drywall and ceiling installation workflows. "
                "We erect heavy-duty metal stud frame networks, hang specialized fire/moisture drywall boards, and lay down extensive high-performance acoustic and thermal insulation batts. "
                "Our tapers and jointers finish with flawless joint sanding, ensuring surfaces are ready for fast decorating."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-brick-wall-icon lucide-brick-wall"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M12 9v6"/><path d="M16 15v6"/><path d="M16 3v6"/><path d="M3 15h18"/><path d="M3 9h18"/><path d="M8 15v6"/><path d="M8 3v6"/></svg>',
            "benefits_list": [
                "Rapid internal room configuration and layout adjustments.",
                "Enforces strict fire-retardant barriers between rooms.",
                "Traps internal ambient heat to cut structural energy waste.",
                "Creates flat, uniform surfaces free from structural buckling.",
                "Conceals ugly electrical feeds and mechanical ventilation lines."
            ]
        },
        {
            "title": "Plastering, Rendering & Surface Skimming",
            "slug": "plastering-rendering-and-surface-skimming",
            "short_desc": "We flatten and restore damaged structural substrates, applying crisp skim coats and external render to establish ideal paint-ready surfaces.",
            "desc": (
                "Achieve flat, flawless, and highly durable surfaces with our professional plastering and rendering services. "
                "We handle premium internal skimming, crisp dry-lining installations, and intensive surface restorations. "
                "For exterior envelopes, our high-grade rendering shields your masonry from weather damage while modernizing your property's exterior aesthetic."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-rectangle-horizontal-icon lucide-rectangle-horizontal"><rect width="20" height="12" x="2" y="6" rx="2"/></svg>',
            "benefits_list": [
                "Creates perfectly smooth surfaces for seamless painting.",
                "Greatly improves property insulation and thermal efficiency.",
                "Effectively seals out external damp and structural moisture.",
                "Modernizes dated brickwork facades and external walls.",
                "Adds an excellent extra layer of internal acoustic soundproofing."
            ]
        },
        {
            "title": "Certified Electrical & Mechanical Engineering",
            "slug": "certified-electrical-and-mechanical-engineering",
            "short_desc": "We eliminate power and gas hazards, implementing fully certified rewires, modern consumer units, and energy-efficient heating networks.",
            "desc": (
                "Our certified electrical and mechanical services provide complete safety, compliance, and modern functionality for your property infrastructure. "
                "We handle everything from full house rewires and consumer unit upgrades to high-efficiency boiler installations and complex central heating layouts. "
                "Every job is strictly tested and certified to adhere to current safety and building regulations."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-cable-icon lucide-cable"><path d="M17 19a1 1 0 0 1-1-1v-2a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2a1 1 0 0 1-1 1z"/><path d="M17 21v-2"/><path d="M19 14V6.5a1 1 0 0 0-7 0v11a1 1 0 0 1-7 0V10"/><path d="M21 21v-2"/><path d="M3 5V3"/><path d="M4 10a2 2 0 0 1-2-2V6a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2a2 2 0 0 1-2 2z"/><path d="M7 5V3"/></svg>',
            "benefits_list": [
                "Full regulatory compliance and safety certification.",
                "Eliminates dangerous fire, electrical shock, and leak hazards.",
                "Reduces energy bills with modern, smart control systems and boilers.",
                "Ensures consistent, reliable power delivery and hot water distribution.",
                "Future-proofs your property for high-load modern appliances."
            ]
        },
        {
            "title": "Glazing, Curtain Walls & Storefront Facades",
            "slug": "glazing-curtain-walls-and-storefront-facades",
            "short_desc": "We reinforce building frontages and optimize daylight capture, installing high-security double/triple glazing with strict weather seals.",
            "desc": (
                "Maximize natural light capture and thermal performance with our advanced glazing solutions. "
                "We coordinate the safe installation of structural double/triple glazed window frameworks, glass bi-fold entries, robust retail storefront facades, and sprawling multistory curtain walls. "
                "Our glass technicians enforce perfect weatherproofing seals and heavy-duty hardware alignment on every pane."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-store-icon lucide-store"><path d="M15 21v-5a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v5"/><path d="M17.774 10.31a1.12 1.12 0 0 0-1.549 0 2.5 2.5 0 0 1-3.451 0 1.12 1.12 0 0 0-1.548 0 2.5 2.5 0 0 1-3.452 0 1.12 1.12 0 0 0-1.549 0 2.5 2.5 0 0 1-3.77-3.248l2.889-4.184A2 2 0 0 1 7 2h10a2 2 0 0 1 1.653.873l2.895 4.192a2.5 2.5 0 0 1-3.774 3.244"/><path d="M4 10.95V19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8.05"/></svg>',
            "benefits_list": [
                "Advanced U-value optimization to trap internal ambient heat.",
                "Outstanding noise reduction from bustling urban streets.",
                "Dramatically maximizes natural day-lighting into core rooms.",
                "High-security toughened glass combinations to stop intrusions.",
                "Imparts a highly striking, modern architectural facade appearance."
            ]
        },
        {
            "title": "Floor Coverings & Wall Tiling Installations",
            "slug": "floor-coverings-and-wall-tiling-installations",
            "short_desc": "We level subfloors and seal wet zones, installing precision-aligned hardwood, porcelain, and safety vinyl to handle heavy daily wear.",
            "desc": (
                "Get a professional surface transformation using our comprehensive covering and tiling services. "
                "We carefully analyze subfloor moisture levels, apply self-leveling screeds, and install premium ceramic, porcelain, solid hardwood, or Luxury Vinyl Tiles (LVT). "
                "From geometric layouts to complete wet-room tanking, we guarantee watertight, long-lasting finishes."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-inspection-panel-icon lucide-inspection-panel"><rect width="18" height="18" x="3" y="3" rx="2"/></svg>',
            "benefits_list": [
                "Flawlessly level surfaces without squeaks or structural dips.",
                "Highly durable composition designed for punishing foot traffic.",
                "Complete water and moisture resistance for wet zones and bathrooms.",
                "Provides an insulated underfoot barrier that dampens impact sound.",
                "Extremely easy to clean and maintain over time."
            ]
        },
        {
            "title": "Fine Painting, Decorating & Coatings",
            "slug": "painting-decorating-and-coatings",
            "short_desc": "We resolve substrate defects via power sanding and priming, delivering premium architectural paint and wallpaper coatings.",
            "desc": (
                "Bring your spaces to life with our comprehensive painting and decorating services. "
                "We specialize in meticulous surface preparation—including power sanding, defect filling, and specialized stain-blocking primers—to guarantee a long-lasting finish. "
                "From interior walls and woodwork trim to weather-resistant exterior rendering coatings and professional wallpaper hanging, we use premium materials to achieve a stunning aesthetic."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-paint-bucket-icon lucide-paint-bucket"><path d="M11 7 6 2"/><path d="M18.992 12H2.041"/><path d="M21.145 18.38A3.34 3.34 0 0 1 20 16.5a3.3 3.3 0 0 1-1.145 1.88c-.575.46-.855 1.02-.855 1.595A2 2 0 0 0 20 22a2 2 0 0 0 2-2.025c0-.58-.285-1.13-.855-1.595"/><path d="m8.5 4.5 2.148-2.148a1.205 1.205 0 0 1 1.704 0l7.296 7.296a1.205 1.205 0 0 1 0 1.704l-7.592 7.592a3.615 3.615 0 0 1-5.112 0l-3.888-3.888a3.615 3.615 0 0 1 0-5.112L5.67 7.33"/></svg>',
            "benefits_list": [
                "Dramatically improves overall property curb appeal.",
                "Complete color and space customization to your unique taste.",
                "Erases surface wear and tear while protecting structural substrates.",
                "Makes aged living and working environments feel brand new.",
                "Boosts competitive buyer interest when listing on the market."
            ]
        },
        {
            "title": "Controlled Demolition & Site Clearance",
            "slug": "controlled-demolition-and-site-clearance",
            "short_desc": "We isolate site hazards and fast-track development timelines, executing clean structural strip-outs and certified waste clearance.",
            "desc": (
                "Prepare your site safely and efficiently with our expert demolition and strip-out services. "
                "We orchestrate controlled structural deconstructions, internal commercial strip-outs, and precise site clearance operations. "
                "Our licensed workflows place critical focus on rigorous safety measures, toxic or hazardous material containment, and maximum recycling of structural wreckage."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-triangle-alert-icon lucide-triangle-alert"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
            "benefits_list": [
                "Maintains rigorous site safety standards to eliminate risk.",
                "Accelerates follow-on construction schedules via fast clearances.",
                "Guarantees fully legal, documented hazardous waste disposal.",
                "Minimizes dust, vibration, and noise impact on neighbors.",
                "Promotes green building via meticulous material salvaging."
            ]
        },
        {
            "title": "Heavy Plant Logistics & Material Handling",
            "slug": "heavy-plant-logistics-and-material-handling",
            "short_desc": "We accelerate mechanical site workflows, mobilizing licensed operators and machinery to safely maneuver massive structural loads.",
            "desc": (
                "Maintain an organized, high-efficiency build site with our general labor and machinery services. "
                "We supply highly skilled, fully licensed operators to manage heavy structural cranes, rough-terrain forklifts, site bulldozers, and deep boring equipment. "
                "By keeping paths clear and staging materials perfectly, we drastically minimize accidents and maximize tool uptime."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-settings-icon lucide-settings"><path d="M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915"/><circle cx="12" cy="12" r="3"/></svg>',
            "benefits_list": [
                "Flawlessly handles and positions massive structural components.",
                "Multiplies structural earth-moving speeds compared to manual work.",
                "Strict adherence to heavy machinery lifting safety protocols.",
                "Maintains an orderly, clean site that cuts safety hazards.",
                "Frees up expensive specialized trades to focus on their core crafts."
            ]
        },
        {
            "title": "Engineering Surveying & Digital Layout Mapping",
            "slug": "engineering-surveying-and-digital-layout-mapping",
            "short_desc": "We erase spatial margins of error, executing millimeter-accurate boundary tracking and laser-guided grid staking to guide your build.",
            "desc": (
                "Erase spatial margins of error with our engineering surveying and layout services. "
                "Using advanced robotic total stations and GPS laser leveling, we map site boundaries, record topographical variances, and establish laser-precise grid staking lines. "
                "This provides your structural, ground, and frame teams with zero-tolerance benchmarks to follow safely."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-locate-fixed-icon lucide-locate-fixed"><line x1="2" x2="5" y1="12" y2="12"/><line x1="19" x2="22" y1="12" y2="12"/><line x1="12" x2="12" y1="2" y2="5"/><line x1="12" x2="12" y1="19" y2="22"/><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="3"/></svg>',
            "benefits_list": [
                "Eliminates expensive building placement or boundary legal disputes.",
                "Guarantees that physical assemblies perfectly match design CAD files.",
                "Provides hyper-accurate calculations for required earthwork shifting.",
                "Establishes precise vertical datums for flawless floor leveling.",
                "Identifies hidden structural or terrain challenges prior to excavation."
            ]
        },
        {
            "title": "Commercial Estimating & Financial Risk Planning",
            "slug": "commercial-estimating-and-financial-risk-planning",
            "short_desc": "We establish bulletproof commercial blueprints, breaking down plans into rigid bills of quantities to insulate you from budget overruns.",
            "desc": (
                "Secure financial clarity for your project before the first shovel hits the dirt. "
                "Our estimating and cost planning services break down architectural plans into precise bills of quantities, tracking market materials variations and structural labor rates. "
                "We establish tight, data-backed cost foundations that guard your budget against unexpected overruns."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-badge-pound-sterling-icon lucide-badge-pound-sterling"><path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="M8 12h4"/><path d="M10 16V9.5a2.5 2.5 0 0 1 5 0"/><path d="M8 16h7"/></svg>',
            "benefits_list": [
                "Provides hyper-realistic, fixed pricing outlines for project bidding.",
                "Identifies value-engineering avenues to reduce cost without dropping quality.",
                "Prevents mid-build cash-flow shortfalls or sudden budget shocks.",
                "Allows for precise material procurement timing to lock in rates.",
                "Provides a clear financial yardstick to track trade outlays."
            ]
        },
        {
            "title": "Project Management & Site Supervision",
            "slug": "turnkey-project-management-and-site-supervision",
            "short_desc": "We control the critical path lifecycle, assigning dedicated foremen to enforce safety, interface with building control, and guarantee delivery.",
            "desc": (
                "Take the stress out of building with our master project management and site supervision frameworks. "
                "We manage critical path timelines, assign and coordinate specialized trade teams, conduct rigorous safety checks, and interface with building inspectors. "
                "We bridge the gap between blueprints and actual site handovers, ensuring a smooth, transparent progression."
            ),
            "svg" : '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-square-chart-gantt-icon lucide-square-chart-gantt"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 8h7"/><path d="M8 12h6"/><path d="M11 16h5"/></svg>',
            "benefits_list": [
                "Delivers complex projects strictly on time and within budget parameters.",
                "Erases client stress via single-point-of-contact site accounting.",
                "Enforces uncompromising quality control and safety standards across all sub-trades.",
                "Catches and fixes minor errors before they impact subsequent construction phases.",
                "Coordinates all legal sign-offs and structural occupancy handovers."
            ]
        }
    ]



    projects_data = [
        {
            "title": "Multi-Unit Flat Renovation",
            "slug": "multi-unit-flat-renovation",
            "short_desc": "Full-scale interior and exterior renovation of a block of residential flats, transforming dilapidated units into modern, compliant, and highly rentable living spaces.",
            "desc": (
                "This extensive project involved the complete strip-out and modernization of a multi-unit residential building, requiring seamless coordination across all major trades. "
                "The structural phase began with precision bricklaying to repair external masonry and alter internal layouts for a more open, efficient floor plan. "
                
            ),
            "featured": True,
            "type": "Residential",
            "units": [
                {
                    "title": "Flat 1a",
                    "description": "The first of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 1b",
                    "description": "The second of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 2",
                    "description": "The third of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 3",
                    "description": "The third of the set of flats, with some extra text here that explains it...",   
                },

            ]
        },
        {
            "title": "Barn Restoration",
            "slug": "historic-barn-restoration-and-landscape-re-engineering",
            "short_desc": "Full-scale structural restoration, internal modernization, and extensive environmental landscaping of a traditional agricultural barn and its surrounding acreage.",
            "desc": (
                "This comprehensive project focused on rescuing and transforming a neglected heritage barn while completely rejuvenating the surrounding topography. "
                "The structural phase required extensive bricklaying and masonry stabilization to rebuild collapsing external walls, mend foundational cracking, and reinforce the primary timber frame supports. "
            ),
            "featured": True,
            "type" : "Residential",
            "units": [
                {
                    "title": "Flat 1a",
                    "description": "The first of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 1b",
                    "description": "The second of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 2",
                    "description": "The third of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 3",
                    "description": "The third of the set of flats, with some extra text here that explains it...",   
                },

            ]
        },
        {
            "title": "Nightclub Build",
            "slug": "nightclub-build-electrical-engineering-and-interior-design",
            "short_desc": "Complete commercial fit-out, advanced electrical infrastructure installation, and bespoke interior design transformation for a premium late-night entertainment venue in Eastbourne.",
            "desc": (
                "This major commercial project involved turning a vacant seaside footprint into a striking, multi-room nightclub experience requiring cutting-edge technological integration and high-end construction. "
                "The build phase commenced with extensive structural partitioning, acoustic soundproofing, and the erection of custom-built feature bars, VIP booths, and a central, reinforced DJ performance stage. "
            ),
            "featured": True,
            "type": "Commerical",
            "units": [
                {
                    "title": "Flat 1a",
                    "description": "The first of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 1b",
                    "description": "The second of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 2",
                    "description": "The third of the set of flats, with some extra text here that explains it...",   
                },
                {
                    "title": "Flat 3",
                    "description": "The third of the set of flats, with some extra text here that explains it...",   
                },

            ]
        }
    ]

    area_data = [
        {
            "title": "Greater London",
            "short_desc": "Comprehensive construction, electrical, plumbing, and decorating services across all London boroughs and commercial zones."
        },
        {
            "title": "Kent",
            "short_desc": "Reliable domestic and commercial trade engineering throughout the Garden of England, including Maidstone, Canterbury, and coastal regions."
        },
        {
            "title": "Sussex",
            "short_desc": "Premium renovations, maintenance, and emergency property services covering East and West Sussex, from Brighton to Eastbourne."
        },
        {
            "title": "Surrey",
            "short_desc": "High-end residential refurbishments, extensions, and structural modernization services throughout Surrey and the surrounding home counties."
        }
    ]

    location_data = [
    # --- Greater London Locations ---
        {
            "area_title": "Greater London",
            "slug" : "croydon-south-east",
            "title": "Croydon & South London",
            "short_description": "Premium domestic extensions, certified electrical rewires, and commercial fit-outs across Croydon and South London.",
            "long_description": "Serving the bustling residential and commercial hubs of South London, our team delivers top-tier structural brickwork, modern plastering, and fully certified gas and electrical engineering. We specialize in adapting period properties for modern living while meeting strict urban building regulations."
        },
        {
            "area_title": "Greater London",
            "slug" : "stratford-east-london",
            "title": "Stratford & East London",
            "short_description": "High-end retail fit-outs, multi-unit apartment modernizations, and professional decorating services.",
            "long_description": "In the rapidly developing landscapes of East London, we provide comprehensive contracting services for both landlords and commercial developers. From full multi-unit flat refurbishments to high-end interior decorating, our multi-trade team ensures swift, premium execution."
        },
        
        # --- Kent Locations ---
        {
            "area_title": "Kent",
            "slug" : "maidestone-central-kent",
            "title": "Maidstone & Central Kent",
            "short_description": "Expert structural alterations, residential plumbing installations, and heritage restoration services.",
            "long_description": "Operating across Maidstone and the heart of Kent, we provide homeowners and businesses with robust property solutions. Our services range from structural brickwork for extensions to complete central heating upgrades and decorative plaster skimming, all backed by industry-leading certifications."
        },
        {
            "area_title": "Kent",
            "slug" : "tumbridge-wells",
            "title": "Tunbridge Wells",
            "short_description": "Bespoke painting and decorating, luxury bathroom installations, and premium residential renovations.",
            "long_description": "Catering to the high-end residential market of Royal Tunbridge Wells, our decorating and plumbing teams specialize in premium finishes. We install luxury bathroom suites, execute flawless wallpapering, and manage meticulous interior transformations with minimal disruption to your home."
        },

        # --- Sussex Locations ---
        {
            "area_title": "Sussex",
            "title": "Brighton & Hove",
            "slug" : "brighton-hove",

            "short_description": "Contemporary commercial refurbishments, emergency plumbing repairs, and architectural plastering.",
            "long_description": "From vibrant seafront commercial venues to historic residential terrace maintenance, our Brighton-based operations cover a diverse array of projects. We provide robust electrical infrastructure updates, comprehensive drainage solutions, and pristine internal rendering."
        },
        {
            "area_title": "Sussex",
            "title": "Eastbourne",
            "slug" : "eastbourne",

            "short_description": "Flagship commercial venue construction, bespoke nightclub builds, and comprehensive local trade support.",
            "long_description": "As the proud home of our major late-night venue project, Eastbourne represents a key service hub. We offer complete multi-trade capabilities here, managing complex commercial electrical engineering grids, structural masonry builds, and durable exterior rendering designed to withstand coastal weather."
        },

        # --- Surrey Locations ---
        {
        "area_title": "Surrey",
        "title": "Guildford & West Surrey",
        "slug" : "guildford-west-surrey",
        "short_description": "Large-scale structural barn restorations, eco-friendly heating upgrades, and complete home modernizations.",
        "long_description": "In Guildford and its surrounding countryside, we handle substantial residential contracts and structural conversions. Our team is expert at integrating discreet, modern electrical and plumbing systems into complex architectural layouts, alongside extensive environmental landscaping."
    }
]

    meta_data = [
        {
            "title": "Welcome to the ROK Group | Premium Construction & Trade Services",
            "description": "The ROK Group delivers expert, fully certified construction, electrical, plumbing, plastering, and decorating services across Greater London and the Home Counties.",
            "keywords": "ROK Group, construction services, commercial fit-out, home renovations, certified electricians, professional plumbing, plastering contracting, London decorators"
        },
        {
            "title": "Our Portfolio | Commercial Builds & Residential Modernization",
            "description": "Explore our recent trade projects, including historic barn restorations, high-end commercial nightclub builds in Eastbourne, and multi-unit flat renovations.",
            "keywords": "construction portfolio, building case studies, nightclub fit-out Eastbourne, barn restoration, structural brickwork examples, ROK Group projects"
        },
        {
            "title": "Our Services | Certified Electrical, Gas, Plumbing & Building",
            "description": "From structural brickwork and flawless plastering to fully certified electrical rewires and comprehensive plumbing, discover our range of premium trade services.",
            "keywords": "accredited electrical engineering, boiler installation, home extensions, plastering rendering, interior decorating, commercial plumbing services"
        },
        {
            "title": "Contact The ROK Group | Request a Project Consultation",
            "description": "Get in touch with our team today for a comprehensive consultation on your upcoming residential or commercial build across London, Kent, Sussex, and Surrey.",
            "keywords": "contact ROK Group, hire builders London, emergency plumbing Sussex, commercial trade quote, request electrical inspection, construction consultation"
        },
        {
            "title": "Areas We Serve | London, Surrey, Kent, Susssex",
            "description": "Looking for reliable tradesmen in Eastbourne and the surrounding areas? The ROK Group provides expert electrical, plumbing, gas, building, and decorating services straight to your doorstep. Check our coverage map and see if we serve your postcode today.",
            "keywords": "ROK Group areas covered, ROK trade services, local plumbers, emergency electrician, builders near me, property maintenance Sussex, multi-trade company Eastbourne, gas engineers near me, local decorators, garden maintenance coverage area"
        },
        {
            "title": "The ROK Blog | Thoughts & Musings from The ROK Team",
            "description": "Get expert home maintenance advice, seasonal property tips, and trade insights from the pros at The ROK Group. Learn how to care for your plumbing, electrics, heating, and garden with our practical guides.",
            "keywords": "The ROK Group blog, home maintenance tips, trade insights Eastbourne, DIY property advice, plumbing guides, electrical safety tips, renovation advice, seasonal garden maintenance, local building advice, ROK group news"
        },
    ]

    page_data = [
        {
            "title": "TRUSTED BUILDERS ACROSS THE SOUTHEAST",
            "tag": "Home",
            "subtitle" : (
                "The Rok Group unifies the full spectrum of trades under one master standard of management."
            )
              
        },
        {
            "title": "Examples of Our Work",
            "tag" : "Projects",
            "subtitle": (
                "A curated showcase of recent projects, highlighting our expertise and the impact we deliver for our clients."
            )

        },
        {
            "title" : "What We Can Do for You",
            "tag": "Services",
            "subtitle" : (
                "Professional electric, plumbing, gas, building, and landscaping services delivered by skilled local tradespeople."
            )
        },
        {
            "title" : "Contact The Rok Group",
            "tag": "Contact",

            "subtitle" : (
                "Ready to start your next project or need a quick repair? Get in touch today for a free, no-obligation quote."
            )
        },
        {
            "title" : "Our Coverage Areas",
            "tag": "Areas",

            "subtitle" : (
                "Proudly delivering professional trade services to homes and businesses across the South East and the surrounding communities."
            )
        },
         {
            "title" : "Latest Articles from Our Blog",
            "tag": "Blog",

            "subtitle" : (
                "Proudly delivering professional trade services to homes and businesses across the South East and the surrounding communities."
            )
        },
    ]
    
    article_data = [
        {
            "title" : "How to spot a cowboy tradesman",
            "slug" : "how-to-spot-a-cowboy-tradesman",
            "subtitle" : "When you're looking for a tradesman, you don't want to be stuck with a cowboy, top tips on how to avoid!",
            "abstract" : "When looking for a new builder, plumber, electrician, or plumber, it can be hard to seperate the good from the bad. Here are 10 top tips to avoid a costly choise mistake.",
            "body_one" : f"""
                    <h1>How to Spot a Cowboy Tradesman</h1>
                    <p class="py-1">If you’re in Eastbourne or anywhere in the South East of England, hiring a reliable tradesman is crucial. Whether you need a plumber, electrician, or builder, the last thing you want is to fall victim to a cowboy tradesman—someone who cuts corners, overcharges, or simply doesn’t deliver. But how can you tell the difference between a trustworthy professional and a cowboy? Let’s dive into some key signs to watch out for, so you can protect your home and your wallet.</p>

                    <h2>What Exactly Is a Cowboy Tradesman?</h2>
                    <p class="py-1">Before we jump into the warning signs, it’s worth clarifying. A cowboy tradesman is not just someone who’s a bit rough around the edges or inexperienced; they’re often unscrupulous, unreliable, and sometimes downright dishonest. They might offer a tempting low quote, but the quality of their work, materials, or customer service leaves a lot to be desired. In the worst cases, they might disappear mid-job or cause more damage than they fix.</p>

                    <h2>Spotting the Red Flags</h2>
                    <p class="py-1">Here are some classic warning signs that you might be dealing with a cowboy tradesman:</p>
                    <ul>
                        <li>Unusually Low Quotes: If a quote sounds too good to be true, it probably is. Cowboy tradesmen often undercut the market to win jobs but then inflate costs with hidden extras or use cheap materials.</li>
                        <li>No Written Contract or Receipt: Always ask for a written quote and a receipt. Cowboys tend to avoid paperwork to dodge accountability.</li>
                        <li>Demanding Full Payment Upfront: Legitimate tradesmen usually ask for a deposit but never the full amount before work starts.</li>
                        <li>Lack of References or Reviews: If they can’t provide previous customer testimonials or have no verifiable online presence, be cautious.</li>
                        <li>Unmarked Vehicles or No ID: Genuine professionals often have branded vehicles and identification badges.</li>
                        <li>Pressure to Start Immediately: Cowboys may push you to make quick decisions or start work without proper planning or permits.</li>
                       
                        <li>Poor Communication: If they’re difficult to contact, don’t return calls, or are vague about timelines, it’s a sign of trouble.</li>
                    </ul>
                    <h2>How to Protect Yourself</h2>
                    <p class="py-1">Now that you know the signs, here are some steps you can take to avoid cowboy tradespeople:</p>
                    <ul>
                        <li>Do Your Homework: Check online reviews, ask friends and neighbours for recommendations, and verify credentials.</li>
                        <li>Get Multiple Quotes: Comparing at least three quotes helps you understand the going rate and spot suspiciously low bids.</li>
                        <li>Ask for Written Estimates and Contracts: Everything should be clear and agreed upon in writing before work begins.</li>
                        <li>Check Insurance and Certifications: Make sure your tradesman is insured and holds any required licences for the job.</li>
                        <li>Trust Your Gut: If something feels off, don’t be afraid to walk away.</li>
                    </ul>
                    Why It Pays to Choose Local and Reputable
                    <p class="py-1">In Eastbourne and the South East, there are plenty of skilled, trustworthy tradespeople who take pride in their work. Choosing someone local not only supports your community but also means they have a reputation to uphold nearby. Plus, they’re more likely to respond promptly and stand behind their work.</p>

                    <p class="py-1">Don’t let cowboy tradesmen spoil your home improvement projects. By staying alert, asking the right questions, and trusting reputable professionals, you can enjoy peace of mind and results that last.</p>

                    <p class="py-1">Next week, we’ll share tips on what questions to ask before hiring any tradesperson—stay tuned!</p>

                    <p class="py-1">Thanks for reading, and here’s to smooth, stress-free projects in Eastbourne and beyond!</p>
            """,
            "author" : "Fred Durst",
            "published_date" : datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
            "blog_form" : "article-short",

            
        },
        {
            "title" : "Top 5 signs your boiler is about to fail",
            "slug" : "top-5-signs-your-boiler-is-about-to-fail",
            "subtitle" : "Don't wait for a winter freeze to find out your boiler is broken, watch for these early warning signs!",
            "abstract" : "A broken boiler can be a costly emergency. Recognizing early symptoms like strange noises or dropping pressure can save you thousands in repairs.",
            "body_one" : "Some text will go here.",
            "author" : "Fred Durst",
            "published_date" : datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
            "blog_form" : "article-short",
        },
        {
            "title" : "How to prepare your garden for a summer deck installation",
            "slug" : "how-to-prepare-your-garden-for-a-summer-deck-installation",
            "subtitle" : "Thinking of adding a decking area? Getting the groundwork right first is crucial for a long-lasting finish.",
            "abstract" : "Before the timber or composite boards arrive, your garden needs proper preparation. Here is how to clear, level, and treat the ground to avoid future rot.",
            "body_one" : "Some text will go here.",
            "author" : "Fred Durst",
            "published_date" : datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
            "blog_form" : "article-short",
        },
        {
            "title" : "Should you DIY your kitchen tiling or hire a professional?",
            "slug" : "should-you-diy-your-kitchen-tiling-or-hire-a-professional",
            "subtitle" : "Tiling looks straightforward on video, but a bad layout can ruin the whole room. Weighing the pros and cons.",
            "abstract" : "While painting or basic shelving are great DIY weekend tasks, tiling a kitchen splashback requires precision. We break down when to save cash or call a pro.",
            "body_one" : "Some text will go here.",
            "author" : "Fred Durst",
            "published_date" : datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
            "blog_form" : "article-short",
        },
        {
            "title" : "Understanding smart home rewiring for older properties",
            "slug" : "understanding-smart-home-rewiring-for-older-properties",
            "subtitle" : "Upgrading an old house with modern tech? Your current consumer unit and wiring might need an upgrade first.",
            "abstract" : "Bringing smart lighting, smart thermostats, and EV chargers into a periodic home is exciting, but safety comes first. Here is what your electrician will look for.",
            "body_one" : "Some text will go here.",
            "author" : "Fred Durst",
            "published_date" : datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
            "blog_form" : "article-short",
        },
        {
            "title" : "How to handle damp and condensation issues before painting",
            "slug" : "how-to-handle-damp-and-condensation-issues-before-painting",
            "subtitle" : "Slapping a fresh coat of paint over a damp patch won't fix it. Learn how to cure the root cause.",
            "abstract" : "Damp walls can cause blistering paint and dangerous mould growth. This guide covers diagnosing penetrative damp versus basic condensation before decorating.",
            "body_one" : "Some text will go here.",
            "author" : "Fred Durst",
            "published_date" : datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day),
            "blog_form" : "article-short",
        },

    ]    

    social_data = [
        {
            'title' : 'Facebook',
            'handle' : '@therokgroup',
            'page_uri' : 'https://www.facebook.com/pages/therokgroup/',
            'icon' : '<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Facebook</title><path d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg>'
        },
        {
            'title' : 'X',
            'handle' : '@therokgroup',
            'page_uri' : 'https://www.x.com/therokgroup/',
            'icon' : '<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>X</title><path d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/></svg>'
        },
        {
            'title' : 'TikTok',
            'handle' : '@therokgroup',
            'page_uri' : 'https://www.tiktok.com/therokgroup/',
            'icon' : '<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>TikTok</title><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>'
        },
         {
            'title' : 'Instagram',
            'handle' : '@therokgroup',
            'page_uri' : 'https://www.instagram.com/users/therokgroup/',
            'icon' : '<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>Instagram</title><path d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg>'
        },


    ]
    
    list_data = [
        {
             "tag" : "home-hero" ,
             "items": [
                    {
                        'order' : 0,
                        'text' : "Residential Experts",
                        'subtext' : "Turnkey delivery of premium architectural properties, structural extensions, and luxury internal refurbs."
                    },
                    {
                        'order' : 1,
                        'text' : "Commercial Knowhow",
                        'subtext' : "Full-scale structural construction, multi-unit developments, retail storefront rollouts, and office strip-outs."
                    },
                     {
                        'order' : 2,
                        'text' : "Personal Rapport",
                        'subtext' : "Transparent communication, dedicated site supervision, and proactive cost planning right from your initial brief."
                    },

             ]
         
        },
        {
            "tag" : "why-rok" ,
             "items": [
                    {
                        'order' : 0,
                        'text' : "Industry Experience",
                        'subtext' : "With over 20 years industry experience.",
                        'svg' : '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-icon lucide-calendar"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>'
                    },
                    {
                        'order' : 1,
                        'text' : "Local Knowledge",
                        'subtext' : "Intimate knowledge of our servicable areas.",
                        'svg' : '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map-pin-icon lucide-map-pin"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>'
                    },
                    {
                        'order' : 2,
                        'text' : "Trusted Tradesmen",
                        'subtext' : "Our workforce is vetted to a high standard.",
                        'svg' : '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield-icon lucide-shield"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>'
                    },
                    {
                        'order' : 3,
                        'text' : "No Obligation Site Visits",
                        'subtext' : "We offer free quotes and honest advice, no strings attached.",
                        'svg' : '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-handshake-icon lucide-handshake"><path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/></svg>'
                    },

             ]
        },
        {
            "tag" : "why-this-matters" ,
             "items": [
                    {
                        'order' : 0,
                        'text' : "Stress Free",
                        'subtext' : "Give yourself one less thing to think about."
                    },
                    {
                        'order' : 1,
                        'text' : "Proven Track Record",
                        'subtext' : "Our projects speak for themselves. We are proud of our work."
                    },
                    {
                        'order' : 2,
                        'text' : "Flexible Schedule",
                        'subtext' : "We can be where you need, when you need us."
                    }

             ]
        },

    ]
    
    policy_data = [
        {
            'title': 'Cookie Policy',
            'nav_title': 'COOKIES',
            'slug' : 'cookies',
            'content' : (
                "Cookie Policy"
                "<p>We use cookies on our website to ensure you get the best experience possible. Cookies are small text files stored on your device that help our website function correctly.</p>"
                "<p>This website exclusively uses functional cookies. These cookies are strictly necessary to provide you with core services and features, such as remembering your preferences, maintaining secure log-in sessions, and ensuring the site loads efficiently. Because these cookies are required for the basic operation of our site, they cannot be disabled.</p>"
                "<p>We do not use any tracking, analytics, targeting, or advertising cookies. Your privacy is fully respected, and no data is shared with third-party tracking services.</p>"
                "<p>By continuing to use our website, you acknowledge and agree to our use of these essential functional cookies. If you have any questions about our cookie usage, please contact our support team.</p>"
            )
        },
        {
            'title': 'Privacy Policy',
            'nav_title': 'PRIVACY',
            'slug' : 'privacy-policy',
            'content' : (
                "<p><strong>Privacy Policy</strong></p>"
                "<p>Your privacy is important to us. This Privacy Policy explains how we collect, use, and protect your personal data when you interact with our website.</p>"
                "<p>Because our website strictly utilizes functional cookies and does not engage in third-party tracking, advertising, or data harvesting, we only collect the minimal personal information necessary to provide our services—such as data you voluntarily provide through contact or login forms.</p>"
                "<p>We take appropriate security measures to prevent unauthorized access, disclosure, or modification of your data. Your information is never sold, rented, or shared with third parties for marketing purposes.</p>"
                "<p>You have the right to access, update, or request the deletion of any personal data we hold about you. If you have any questions regarding your privacy, please feel free to reach out to our team.</p>"
            )
        },
        {
            'title': 'Terms of Service',
            'nav_title': 'TERMS',
            'slug' : 'terms',
            'content' : (
                "<p><strong>Terms of Service</strong></p>"
                "<p>Welcome to our website. By accessing or using our services, you agree to be bound by these Terms of Service and all applicable laws and regulations.</p>"
                "<p>The content, tools, and services provided on this website are for your general information and professional use. Unauthorized use of this website, including attempting to disrupt its security or reverse-engineer its features, is strictly prohibited.</p>"
                "<p>We strive to ensure the website is reliable and accessible, but we provide our services on an 'as-is' and 'as-available' basis without warranties of any kind. We reserve the right to modify or discontinue services at any time without prior notice.</p>"
                "<p>We reserve the right to update these terms periodically. Your continued use of the website following any changes constitutes acceptance of the revised Terms of Service.</p>"
            )
        }
    ]
    
    # 2. Process and insert Services
    print("Populating Services...")
    for item in services_data:
        existing_service = Service.query.filter_by(slug=item["slug"]).first()
        if not existing_service:
            list_title = item['title']+ " Benefits"
            new_list = List(
                tag=list_title
            )
            db.session.add(new_list)
            db.session.flush()
            order = 0
            for benefit in item['benefits_list']:
                list_ben = ListItem(
                    order=order,
                    text=benefit,
                    list_id=new_list.id,
                )
                db.session.add(list_ben)
                order += 1
            db.session.flush()
            new_service = Service(
                title=item["title"],
                slug=item["slug"],
                short_desc=item["short_desc"],
                desc=item["desc"],
                svg=item['svg'],
                benefits_list_id = new_list.id,
            )
            db.session.add(new_service)
            print(f" -> Added Service: {item['title']} [{item['slug']}]")
        else:
            print(f" -> Service already exists: {item['slug']}")


    # 4. Process and insert Locations
    print("Populating Locations...")
    for item in area_data:
        # Check if the location already exists to avoid duplication
        existing_location = Area.query.filter_by(title=item["title"]).first()
        if not existing_location:
            new_location = Area(
                title=item["title"],
                short_desc=item["short_desc"]
            )
            db.session.add(new_location)
            print(f" -> Added Location: {item['title']}")
        else:
            print(f" -> Location already exists: {item['title']}")


    # 2. Populate the sub-locations using Foreign Key lookups
    print("Populating Sub-Locations...")
    for l_item in location_data:
        # Prevent duplicate location entries
        existing_location = Location.query.filter_by(title=l_item["title"]).first()
        
        if not existing_location:
            # Find the parent Area record matching the area_title string
            parent_area = Area.query.filter_by(title=l_item["area_title"]).first()
            
            if parent_area:
                new_location = Location(
                    area_id=parent_area.id, # Map the foreign key dynamically
                    title=l_item["title"],
                    short_description=l_item["short_description"],
                    long_description=l_item["long_description"],
                    slug=l_item['slug']
                )
                db.session.add(new_location)
                print(f" -> Added Location: '{l_item['title']}' under Area: '{l_item['area_title']}'")
            else:
                print(f" !! Warning: Parent Area '{l_item['area_title']}' not found for location '{l_item['title']}'")
        else:
            print(f" -> Location '{l_item['title']}' already exists. Skipping.")



    # 3. Process and insert Projects
    print("Populating Projects...")
    all_services = Service.query.limit(4).all()
    first_location = Location.query.first()
    for item in projects_data:
        existing_project = Project.query.filter_by(slug=item["slug"]).first()
        if not existing_project:
            new_project : Project = Project(
                title=item["title"],
                slug=item["slug"],
                short_desc=item["short_desc"],
                desc=item["desc"],
                featured=item["featured"],
                type = item["type"]
            )
            new_project.services.extend(all_services)
            new_project.location = first_location
            db.session.add(new_project)
            db.session.flush()
            if 'units' in item.keys():
                for unit in item['units']:
                    new_unit : Unit = Unit(
                        title=unit['title'],
                        description=unit['description'],
                        project_id=new_project.id, 

                    )
                    db.session.add(new_unit)
            print(f" -> Added Project: {item['title']} [{item['slug']}]")
        else:
            print(f" -> Project already exists: {item['slug']}")



    print("🌱 Starting article seeding...")
    
    # 2. Use a loop to instantiate your models and track them in a list
    new_articles = []
    for data in article_data:
        # Check if an article with the same slug already exists to prevent crashes
        existing_article = Article.query.filter_by(slug=data['slug']).first()
        
        if not existing_article:
            # The **data syntax unpacks your dictionary straight into the model fields
            article = Article(**data)
            new_articles.append(article)
            print(f"Adding: {data['title']}")
        else:
            print(f"Skipping (Slug already exists): {data['title']}")

    # 3. Add and commit all new records in a single transaction
    if new_articles:
        db.session.add_all(new_articles)
        db.session.commit()
        print(f"🎉 Successfully seeded {len(new_articles)} new articles!")
    else:
        print("Done! No new articles needed to be added.")

    # Final commit to save all locations securely
    db.session.commit()
    print("Location hierarchy successfully seeded!")

    print("Populating Pages and Meta Records...")
    
    # zip() lets us loop through both data arrays side-by-side seamlessly
    for p_info, m_info in zip(page_data, meta_data):
        
        # Prevent duplicates by validating if the page title already exists
        existing_page = Page.query.filter_by(title=p_info["title"]).first()
        
        if not existing_page:
            # 1. Instantiate the Meta record first
            new_meta = Meta(
                title=m_info["title"],
                keywords=m_info["keywords"],
                description=m_info["description"]
            )
            db.session.add(new_meta)
            
            # Flush changes so SQLAlchemy fetches the newly generated meta ID 
            # from the database pool without ending the current transaction block
            db.session.flush()
            
            # 2. Instantiate the Page record and inject the fresh meta ID relationship
            new_page = Page(
                title=p_info["title"],
                subtitle=p_info["subtitle"],
                tag=p_info["tag"],
                meta_id=new_meta.id
            )
            db.session.add(new_page)
            print(f" -> Added Page: '{p_info['title']}' linked to its One-to-One Meta profile.")
        else:
            print(f" -> Page entry '{p_info['title']}' already exists. Skipping.")


    print("Populating socials")
    for data in social_data:
        existing_social = Social.query.filter_by(title=data['title']).first()
        if not existing_social:
            new_social = Social(**data)
            db.session.add(new_social)
            print(f" -> Added Social '{new_social.title}'")


    # 4. Commit changes to the database
    db.session.commit()
    print("Database successfully seeded with unique entries!")

    print("Adding Static List Items.")

    for lst in list_data:
        existing_list = List.query.filter_by(tag=lst['tag']).first()
        if not existing_list:
            new_list = List(tag=lst['tag'])
            db.session.add(new_list)
            db.session.flush()
            for item in lst.get('items', []):
                new_list_item = ListItem(
                    order=item.get('order', 0),
                    text=item.get('text', ''),
                    subtext=item.get('subtext'),
                    list_id=new_list.id,
                    svg=item.get('svg', '')
                )
                db.session.add(new_list_item)
    db.session.commit()

    for policy in policy_data:
        existing_policy =  Policy.query.filter_by(title=policy['title']).first()
        if not existing_policy:
            new_policy = Policy(
                title=policy['title'],
                nav_title=policy['nav_title'],
                content=policy['content'],
                slug=policy['slug']
            )
            db.session.add(new_policy)

    db.session.commit()
        

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_database()