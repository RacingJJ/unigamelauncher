import { useState } from 'react'
import { Bell, ChevronDown, Grid2X2, House, Library, Plus, Search, Settings, SlidersHorizontal, Sparkles } from 'lucide-react'

type Game = {
  title: string
  source: 'Steam' | 'Epic' | 'Roblox' | 'itch.io' | 'PC'
  accent: string
  image: string
}

const games: Game[] = [
  { title: 'Elden Ring', source: 'Steam', accent: '#b48a55', image: 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=900&auto=format&fit=crop' },
  { title: 'Cyberpunk 2077', source: 'Steam', accent: '#e7c72f', image: 'https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=900&auto=format&fit=crop' },
  { title: 'Forza Horizon 5', source: 'Steam', accent: '#d96ac3', image: 'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?w=900&auto=format&fit=crop' },
  { title: 'Fortnite', source: 'Epic', accent: '#846fd7', image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?w=900&auto=format&fit=crop' },
  { title: 'Hades II', source: 'PC', accent: '#9e3f58', image: 'https://images.unsplash.com/photo-1519608487953-e999c86e7455?w=900&auto=format&fit=crop' },
  { title: 'Celeste', source: 'itch.io', accent: '#73a5b5', image: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=900&auto=format&fit=crop' },
]

export default function App() {
  const [query, setQuery] = useState('')
  const [active, setActive] = useState('Library')
  const visible = games.filter(game => game.title.toLowerCase().includes(query.toLowerCase()))

  return (
    <main className="app">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark"><Sparkles size={19} /></div><span>UniGame</span></div>
        <nav>
          <button className={active === 'Home' ? 'active' : ''} onClick={() => setActive('Home')}><House /> Home</button>
          <button className={active === 'Library' ? 'active' : ''} onClick={() => setActive('Library')}><Library /> Library <span className="count">6</span></button>
          <button className={active === 'Discover' ? 'active' : ''} onClick={() => setActive('Discover')}><Grid2X2 /> Discover</button>
        </nav>
        <div className="sidebar-bottom">
          <button><Settings /> Settings</button>
        </div>
      </aside>

      <section className="content">
        <header>
          <div className="search"><Search /><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search games" /></div>
          <button className="icon-button" aria-label="Notifications"><Bell /></button>
          <button className="profile"><span>R</span><ChevronDown /></button>
        </header>

        <div className="page-heading">
          <div><p className="eyebrow">MY COLLECTION</p><h1>Library</h1></div>
          <div className="actions"><button className="filter"><SlidersHorizontal /> Filter</button><button className="add"><Plus /> Add game</button></div>
        </div>

        <div className="tabs"><button className="selected">All games <span>6</span></button><button>Recently played</button><button>Favorites</button></div>

        <div className="game-grid">
          {visible.map(game => (
            <article className="game-card" key={game.title}>
              <button className="game-cover" style={{ background: `linear-gradient(145deg, ${game.accent}55, #17191d), url(${game.image}) center/cover` }}>
                <span className="play">▶</span>
              </button>
              <div className="game-info"><div><h3>{game.title}</h3><p>{game.source}</p></div><button aria-label={`More options for ${game.title}`}>•••</button></div>
            </article>
          ))}
        </div>
      </section>
    </main>
  )
}
