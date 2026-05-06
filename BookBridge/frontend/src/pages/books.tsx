import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { booksAPI } from '@/services/api';

interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  description: string;
  total_copies: number;
  available_copies: number;
}

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formVisible, setFormVisible] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    isbn: '',
    description: '',
    total_copies: 1,
  });

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      const response = await booksAPI.getAll();
      setBooks(response.data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch books');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await booksAPI.create(formData);
      setFormData({
        title: '',
        author: '',
        isbn: '',
        description: '',
        total_copies: 1,
      });
      setFormVisible(false);
      fetchBooks();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create book');
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure?')) {
      try {
        await booksAPI.delete(id);
        fetchBooks();
      } catch (err: any) {
        setError('Failed to delete book');
      }
    }
  };

  return (
    <>
      <Head>
        <title>Books - BookBridge</title>
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link href="/" className="text-2xl font-bold text-indigo-600">
                  📚 BookBridge
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link href="/" className="text-gray-600 hover:text-indigo-600">
                  Home
                </Link>
                <Link href="/members" className="text-gray-600 hover:text-indigo-600">
                  Members
                </Link>
                <Link href="/borrowings" className="text-gray-600 hover:text-indigo-600">
                  Borrowings
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Books</h1>
            <button
              onClick={() => setFormVisible(!formVisible)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            >
              {formVisible ? 'Cancel' : 'Add Book'}
            </button>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {formVisible && (
            <div className="mb-8 p-6 bg-white rounded-lg shadow">
              <h2 className="text-xl font-bold mb-4">Add New Book</h2>
              <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Title"
                    value={formData.title}
                    onChange={(e) =>
                      setFormData({ ...formData, title: e.target.value })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                    required
                  />
                  <input
                    type="text"
                    placeholder="Author"
                    value={formData.author}
                    onChange={(e) =>
                      setFormData({ ...formData, author: e.target.value })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                    required
                  />
                  <input
                    type="text"
                    placeholder="ISBN"
                    value={formData.isbn}
                    onChange={(e) =>
                      setFormData({ ...formData, isbn: e.target.value })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                    required
                  />
                  <input
                    type="number"
                    placeholder="Total Copies"
                    min="1"
                    value={formData.total_copies}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        total_copies: parseInt(e.target.value),
                      })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                  />
                  <textarea
                    placeholder="Description"
                    value={formData.description}
                    onChange={(e) =>
                      setFormData({ ...formData, description: e.target.value })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600 md:col-span-2"
                    rows={3}
                  />
                </div>
                <button
                  type="submit"
                  className="mt-4 w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700"
                >
                  Add Book
                </button>
              </form>
            </div>
          )}

          {loading ? (
            <div className="text-center py-8">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {books.map((book) => (
                <div
                  key={book.id}
                  className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition"
                >
                  <h3 className="text-lg font-bold text-gray-900 mb-2">
                    {book.title}
                  </h3>
                  <p className="text-gray-600 mb-2">by {book.author}</p>
                  <p className="text-sm text-gray-500 mb-3">ISBN: {book.isbn}</p>
                  {book.description && (
                    <p className="text-gray-700 mb-3 text-sm">
                      {book.description}
                    </p>
                  )}
                  <div className="mb-4 p-3 bg-blue-50 rounded">
                    <p className="text-sm">
                      <span className="font-bold">Total:</span> {book.total_copies}
                    </p>
                    <p className="text-sm">
                      <span className="font-bold">Available:</span>{' '}
                      {book.available_copies}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(book.id)}
                    className="w-full bg-red-600 text-white py-2 rounded-lg hover:bg-red-700"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
