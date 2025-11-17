import React, { useEffect, useState } from 'react';

const pageSize = 10;

export default function CharitiesList() {
  const [items, setItems] = useState([]);
  const [count, setCount] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [location, setLocation] = useState('');

  const fetchCharities = async (pageNum = 1) => {
    setLoading(true);
    const params = new URLSearchParams();
    params.set('page', pageNum.toString());
    if (search) params.set('search', search);
    if (category) params.set('category', category);
    if (location) params.set('location', location);

    const res = await fetch(`/api/charities/?${params.toString()}`);
    const data = await res.json();
    setItems(data.results || []);
    setCount(data.count || 0);
    setPage(pageNum);
    setLoading(false);
  };

  useEffect(() => {
    fetchCharities(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const totalPages = Math.ceil(count / pageSize) || 1;

  return (
    <div className="container" style={{ maxWidth: 1100, margin: '0 auto', padding: 24 }}>
      <h2 style={{ fontSize: 28, fontWeight: 800, marginBottom: 12 }}>Charities</h2>

      {/* Filters */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr auto', gap: 12, marginBottom: 16 }}>
        <input
          placeholder="Search by name/location..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: 10, borderRadius: 8, border: '1px solid #ddd' }}
        />
        <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ padding: 10, borderRadius: 8, border: '1px solid #ddd' }}>
          <option value="">All Categories</option>
          <option value="education">Education</option>
          <option value="health">Health</option>
          <option value="women_support">Women Support</option>
          <option value="other">Other</option>
        </select>
        <input
          placeholder="Filter by location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          style={{ padding: 10, borderRadius: 8, border: '1px solid #ddd' }}
        />
        <button onClick={() => fetchCharities(1)} style={{ padding: '10px 16px', borderRadius: 8, background: '#16a34a', color: '#fff', border: 0, fontWeight: 700 }}>Apply</button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
          {items.map((c) => (
            <div key={c.id} style={{ background: '#fff', borderRadius: 12, overflow: 'hidden', boxShadow: '0 8px 18px rgba(0,0,0,0.08)' }}>
              <div style={{ background: '#f8fafc', height: 140, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {c.logo ? (
                  <img alt={c.name} src={c.logo} style={{ maxHeight: 110, maxWidth: '90%', objectFit: 'contain' }} />
                ) : (
                  <div style={{ color: '#94a3b8' }}>No Logo</div>
                )}
              </div>
              <div style={{ padding: 14 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <h3 style={{ margin: 0, fontSize: 18 }}>{c.name}</h3>
                  <span style={{ background: '#eef2ff', color: '#4338ca', padding: '4px 10px', borderRadius: 999, fontSize: 12, fontWeight: 700 }}>{c.category}</span>
                </div>
                <div style={{ color: '#64748b', fontSize: 13, marginTop: 6 }}>{c.location || '—'}</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginTop: 12 }}>
                  {c.link ? (
                    <a href={c.link} target="_blank" rel="noopener" style={{ textAlign: 'center', padding: 10, borderRadius: 10, border: '2px solid #6366f1', color: '#4f46e5', fontWeight: 700, textDecoration: 'none' }}>Know More</a>
                  ) : (
                    <button disabled style={{ textAlign: 'center', padding: 10, borderRadius: 10, border: '2px solid #e5e7eb', color: '#9ca3af', fontWeight: 700, background: 'transparent' }}>Know More</button>
                  )}
                  <button style={{ textAlign: 'center', padding: 10, borderRadius: 10, background: '#16a34a', color: '#fff', fontWeight: 700, border: 0 }}>Donate</button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      <div style={{ display: 'flex', gap: 8, justifyContent: 'center', marginTop: 16 }}>
        <button disabled={page <= 1} onClick={() => fetchCharities(page - 1)} style={{ padding: '8px 12px' }}>Prev</button>
        <div style={{ padding: '8px 12px' }}>{page} / {totalPages}</div>
        <button disabled={page >= totalPages} onClick={() => fetchCharities(page + 1)} style={{ padding: '8px 12px' }}>Next</button>
      </div>
    </div>
  );
}
