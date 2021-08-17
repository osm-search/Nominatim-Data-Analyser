import { usePromiseTracker } from "react-promise-tracker";
import Loader from 'react-loader-spinner';

/**
 * Loading indicator for when we are waiting for a promise.
 */
const LoadingIndicator = ( {area, size, className} ) => {
    const { promiseInProgress } = usePromiseTracker({area: area});
    return (
        <div>
            {promiseInProgress && 
            <div className={className}>
                <Loader type="ThreeDots" color="#82b9ff" height={size} width={size} />
            </div>
            }
        </div>
    )
}

export default LoadingIndicator
