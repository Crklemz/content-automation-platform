'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Site } from '@/types';

interface SiteNavigationProps {
  currentSite: Site;
  allSites: Site[];
}

export default function SiteNavigation({ currentSite, allSites }: SiteNavigationProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Current Site */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center">
              <div 
                className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm mr-3"
                style={{ backgroundColor: currentSite.primary_color }}
              >
                C
              </div>
              <span className="text-lg font-semibold text-gray-900">
                Content Platform
              </span>
            </Link>
            <div className="ml-6 flex items-center">
              <span className="text-gray-400 mx-2">•</span>
              <span 
                className="font-medium"
                style={{ color: currentSite.primary_color }}
              >
                {currentSite.name}
              </span>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              href="/" 
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              All Sites
            </Link>
            
            {/* Site Dropdown */}
            <div className="relative group">
              <button className="flex items-center text-gray-600 hover:text-gray-900 transition-colors">
                <span>Switch Site</span>
                <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {/* Dropdown Menu */}
              <div className="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                <div className="py-2">
                  {allSites.map((site) => (
                    <Link
                      key={site.slug}
                      href={`/${site.slug}`}
                      className={`flex items-center px-4 py-2 text-sm hover:bg-gray-50 transition-colors ${
                        site.slug === currentSite.slug ? 'bg-gray-50' : ''
                      }`}
                    >
                      <div 
                        className="w-6 h-6 rounded flex items-center justify-center text-white text-xs font-bold mr-3"
                        style={{ backgroundColor: site.primary_color }}
                      >
                        {site.name.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">{site.name}</div>
                        <div className="text-xs text-gray-500 truncate">{site.description}</div>
                      </div>
                      {site.slug === currentSite.slug && (
                        <svg className="w-4 h-4 text-green-500 ml-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </Link>
                  ))}
                </div>
              </div>
            </div>

            <Link 
              href="/admin" 
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              Admin
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4">
            <div className="space-y-2">
              <Link 
                href="/" 
                className="block px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                All Sites
              </Link>
              
              <div className="px-4 py-2">
                <div className="text-sm font-medium text-gray-700 mb-2">Switch Site:</div>
                <div className="space-y-1">
                  {allSites.map((site) => (
                    <Link
                      key={site.slug}
                      href={`/${site.slug}`}
                      className={`flex items-center px-2 py-1 text-sm rounded transition-colors ${
                        site.slug === currentSite.slug 
                          ? 'bg-gray-100 text-gray-900' 
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                      }`}
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <div 
                        className="w-5 h-5 rounded flex items-center justify-center text-white text-xs font-bold mr-2"
                        style={{ backgroundColor: site.primary_color }}
                      >
                        {site.name.charAt(0).toUpperCase()}
                      </div>
                      <span className="truncate">{site.name}</span>
                    </Link>
                  ))}
                </div>
              </div>

              <Link 
                href="/admin" 
                className="block px-4 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Admin
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
} 