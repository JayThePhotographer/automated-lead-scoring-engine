import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import Image from 'next/image';

// Fetch data directly from SQLite
async function getLeads() {
  const db = await open({
    filename: './leads.db',
    driver: sqlite3.Database
  });

  const leads = await db.all(`
    SELECT c.id, c.company_name, c.website_url, c.overall_score, m.image_url, m.deficit_tag
    FROM companies c
    LEFT JOIN media_audits m ON c.id = m.company_id
    GROUP BY c.id
    ORDER BY c.overall_score DESC
  `);
  
  return leads;
}

export default async function Dashboard() {
  const leads = await getLeads();

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        
        {/* Header section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Automated Prospecting Engine</h1>
          <p className="text-gray-500 mt-2">Internal Lead Scoring Dashboard v1.0</p>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Scraped Asset</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Identified Deficit</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Lead Score</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {leads.map((lead: any) => (
                <tr key={lead.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap border-b border-gray-100">
                    <div className="text-sm font-semibold text-gray-900 capitalize">{lead.company_name}</div>
                    <a href={lead.website_url} target="_blank" rel="noreferrer text-blue-500 hover:underline text-xs">
                      {lead.website_url}
                    </a>
                  </td>
                  <div className="flex h-16 w-24 overflow-hidden rounded bg-gray-100 border border-gray-200 mt-4 ml-6">
                    {lead.image_url ? (
                      <img src={lead.image_url} alt="Scraped asset" className="object-cover h-full w-full opacity-90 hover:opacity-100 transition-opacity" />
                    ) : (
                      <span className="text-xs text-gray-400 m-auto">No Image</span>
                    )}
                  </div>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                      {lead.deficit_tag}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 border-b border-gray-100">
                    <div className="flex items-center">
                      <div className="h-2.5 w-2.5 rounded-full bg-orange-500 mr-2"></div>
                      <span className="font-bold text-gray-700">{lead.overall_score} / 10</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium border-b border-gray-100">
                    <button className="text-indigo-600 hover:text-indigo-900 bg-indigo-50 px-3 py-1 rounded-md transition-colors">
                      Push to CRM
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </div>
  );
}