using System;

namespace SWpart2
{
    public abstract class OpenFigure : IShape
    {
        public virtual double square()
        {
            return 0;
        }

        public  virtual double length()
        {
            throw new NotImplementedException();
        }

        public virtual bool cross(IShape i)
        {
            throw new NotImplementedException();
        }

        public virtual IShape shift(Point2D a)
        {
            throw new NotImplementedException();
        }

        public virtual IShape rot(double phi)
        {
            throw new NotImplementedException();
        }

        public virtual IShape symAxis(int i)
        {
            throw new NotImplementedException();
        }
    }
}