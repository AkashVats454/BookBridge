import { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { borrowingsAPI, booksAPI, membersAPI } from '@/services/api';

interface Borrowing {
  id: number;
  book_id: number;
  member_id: number;
  borrowed_date: string;
  due_date: string;
  returned_date: string | null;
  is_returned: boolean;
  is_overdue: boolean;
}

interface Book {
  id: number;
  title: string;
}

interface Member {
  id: number;
  name: string;
}

export default function BorrowingsPage() {
  const [borrowings, setborrowings] = useState<Borrowing[]>([]);
  const [books, setBooks] = useState<Book[]>([]);
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formVisible, setFormVisible] = useState(false);
  const [showOnlyActive, setShowOnlyActive] = useState(true);
  const [formData, setFormData] = useState({
    book_id: '',
    member_id: '',
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [borrowingsRes, booksRes, membersRes] = await Promise.all([
        borrowingsAPI.getAll(),
        booksAPI.getAll(0, 100),
        membersAPI.getAll(0, 100),
      ]);
      setborrowings(borrowingsRes.data);
      setBooks(booksRes.data);
      setMembers(membersRes.data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await borrowingsAPI.borrow({
        book_id: parseInt(formData.book_id),
        member_id: parseInt(formData.member_id),
      });
      setFormData({ book_id: '', member_id: '' });
      setFormVisible(false);
      fetchData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to record borrowing');
    }
  };

  const handleReturn = async (id: number) => {
    try {
      await borrowingsAPI.returnBook(id);
      fetchData();
    } catch (err: any) {
      setError('Failed to return book');
    }
  };

  const filteredBorrowings = showOnlyActive
    ? borrowings.filter((b) => !b.is_returned)
    : borrowings;

  const getBookTitle = (bookId: number) => {
    return books.find((b) => b.id === bookId)?.title || 'Unknown';
  };

  const getMemberName = (memberId: number) => {
    return members.find((m) => m.id === memberId)?.name || 'Unknown';
  };

  return (
    <>
      <Head>
        <title>Borrowings - BookBridge</title>
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
                <Link href="/books" className="text-gray-600 hover:text-indigo-600">
                  Books
                </Link>
                <Link href="/members" className="text-gray-600 hover:text-indigo-600">
                  Members
                </Link>
              </div>
            </div>
          </div>
        </nav>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Borrowings</h1>
            <button
              onClick={() => setFormVisible(!formVisible)}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
            >
              {formVisible ? 'Cancel' : 'Record Borrowing'}
            </button>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {formVisible && (
            <div className="mb-8 p-6 bg-white rounded-lg shadow">
              <h2 className="text-xl font-bold mb-4">Record Book Borrowing</h2>
              <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <select
                    value={formData.book_id}
                    onChange={(e) =>
                      setFormData({ ...formData, book_id: e.target.value })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                    required
                  >
                    <option value="">Select a Book</option>
                    {books.map((book) => (
                      <option key={book.id} value={book.id}>
                        {book.title}
                      </option>
                    ))}
                  </select>
                  <select
                    value={formData.member_id}
                    onChange={(e) =>
                      setFormData({ ...formData, member_id: e.target.value })
                    }
                    className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-600"
                    required
                  >
                    <option value="">Select a Member</option>
                    {members.map((member) => (
                      <option key={member.id} value={member.id}>
                        {member.name}
                      </option>
                    ))}
                  </select>
                </div>
                <button
                  type="submit"
                  className="mt-4 w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700"
                >
                  Record Borrowing
                </button>
              </form>
            </div>
          )}

          <div className="mb-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showOnlyActive}
                onChange={(e) => setShowOnlyActive(e.target.checked)}
                className="mr-2"
              />
              <span className="text-gray-700">Show only active borrowings</span>
            </label>
          </div>

          {loading ? (
            <div className="text-center py-8">Loading...</div>
          ) : (
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-900">
                      Book
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-900">
                      Member
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-900">
                      Borrowed Date
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-900">
                      Due Date
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-900">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-sm font-medium text-gray-900">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredBorrowings.map((borrowing) => (
                    <tr key={borrowing.id}>
                      <td className="px-6 py-4 text-sm font-medium text-gray-900">
                        {getBookTitle(borrowing.book_id)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {getMemberName(borrowing.member_id)}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {new Date(borrowing.borrowed_date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        <span
                          className={
                            borrowing.is_overdue && !borrowing.is_returned
                              ? 'text-red-600 font-bold'
                              : ''
                          }
                        >
                          {new Date(borrowing.due_date).toLocaleDateString()}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${
                            borrowing.is_returned
                              ? 'bg-green-100 text-green-800'
                              : borrowing.is_overdue
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {borrowing.is_returned
                            ? 'Returned'
                            : borrowing.is_overdue
                            ? 'Overdue'
                            : 'Active'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        {!borrowing.is_returned && (
                          <button
                            onClick={() => handleReturn(borrowing.id)}
                            className="text-green-600 hover:text-green-900"
                          >
                            Return
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
