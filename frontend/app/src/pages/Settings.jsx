const Settings = () => {
    const userId = sessionStorage.getItem("userId");

    return (
        <div className="p-6 max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold mb-4">Settings</h2>
            <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700">User ID: <span className="font-mono">{userId}</span></p>
            </div>
        </div>
    );
};

export default Settings;