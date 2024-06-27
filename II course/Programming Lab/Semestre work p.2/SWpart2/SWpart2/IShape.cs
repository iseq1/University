namespace SWpart2
{
    public interface IShape
    {
        double square();

        double length();

        bool cross(IShape i);
        
        IShape shift(Point2D a);

        IShape rot(double phi);

        IShape symAxis(int i);
    }
}