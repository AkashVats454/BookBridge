import Head from 'next/head';
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <Head>
        <title>BookBridge - Library Management System</title>
        <meta name="description" content="Library Management System" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Navigation */}
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <span className="text-2xl font-bold text-indigo-600">📚 BookBridge</span>
              </div>
              <div className="hidden md:flex space-x-8">
                <Link href="/books" className="text-gray-700 hover:text-indigo-600">
                  Books
                </Link>
                <Link href="/members" className="text-gray-700 hover:text-indigo-600">
                  Members
                </Link>
                <Link href="/borrowings" className="text-gray-700 hover:text-indigo-600">
                  Borrowings
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              Welcome to BookBridge
            </h1>
            <p className="text-xl text-gray-700 mb-8">
              A modern library management system for tracking books, members, and borrowing operations
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
              {/* Books Card */}
              <Link href="/books">
                <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition cursor-pointer">
                  <div className="text-4xl mb-4">📖</div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Books</h2>
                  <p className="text-gray-600">
                    Manage your library catalog - add, edit, and track all books
                  </p>
                </div>
              </Link>

              {/* Members Card */}
              <Link href="/members">
                <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition cursor-pointer">
                  <div className="text-4xl mb-4">👥</div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Members</h2>
                  <p className="text-gray-600">
                    Keep track of library members and their information
                  </p>
                </div>
              </Link>

              {/* Borrowings Card */}
              <Link href="/borrowings">
                <div className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition cursor-pointer">
                  <div className="text-4xl mb-4">📋</div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Borrowings</h2>
                  <p className="text-gray-600">
                    Record and track book borrowing and return operations
                  </p>
                </div>
              </Link>
            </div>

            {/* Quick Stats */}
            <div className="mt-20">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Quick Start</h3>
              <p className="text-gray-700 mb-8">
                Use the navigation above or click on any card to get started
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
