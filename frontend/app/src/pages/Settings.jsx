
const Settings = () => {
    const userId = sessionStorage.getItem("userId");

    return (
        <div>
            <p>User ID: {userId}</p>
        </div>
    );
};

export default Settings;