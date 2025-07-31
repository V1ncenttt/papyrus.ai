export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            Welcome to <span className="text-indigo-600">ScholarMind</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            AI-powered research paper analysis and knowledge extraction platform. 
            Search, analyze, and chat with your research papers.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="bg-blue-500 rounded-lg p-3 w-fit text-white mb-4">
              📄
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Papers</h3>
            <p className="text-gray-600">Upload research papers and let AI extract key insights and information.</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="bg-green-500 rounded-lg p-3 w-fit text-white mb-4">
              🔍
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Semantic Search</h3>
            <p className="text-gray-600">Find relevant papers and sections using intelligent semantic search.</p>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="bg-purple-500 rounded-lg p-3 w-fit text-white mb-4">
              💬
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Chat</h3>
            <p className="text-gray-600">Chat with your papers and get instant answers to research questions.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
