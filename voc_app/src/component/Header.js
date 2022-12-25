import { Link } from "react-router-dom";

export default function Header() {
    return (
        <div className="header">
            <h1>
                <Link to="/"> Vocabulaire français </Link>
            </h1>

            <div className="menu">
                <a href="#x" className="link">
                    Ajouter un mot
                </a>
                <a href="#x" className="link">
                    Ajouter un jour
                </a>
            </div>
        </div>);
}   