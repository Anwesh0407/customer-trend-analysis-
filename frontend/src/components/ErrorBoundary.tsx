import { Component, type ErrorInfo, type ReactNode } from 'react';
import { AlertTriangle, RotateCcw, Home, ChevronDown, ChevronUp } from 'lucide-react';

interface Props {
  children: ReactNode;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
  showDetails: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
    showDetails: false,
  };

  public static getDerivedStateFromError(error: Error): Partial<State> {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('AVA ErrorBoundary caught an unhandled render error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null, showDetails: false });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="max-w-3xl mx-auto my-12 p-8 bg-white border border-red-200 rounded-2xl shadow-sm text-center space-y-6">
          <div className="w-14 h-14 mx-auto rounded-full bg-red-50 border border-red-200 flex items-center justify-center text-red-600">
            <AlertTriangle className="w-7 h-7" />
          </div>

          <div className="space-y-2">
            <h2 className="text-xl font-bold text-gray-900 tracking-tight">
              Interface Display Recovery
            </h2>
            <p className="text-sm text-gray-600 max-w-lg mx-auto">
              We prevented a screen crash. The workspace encountered unexpected data formatting and safely stopped rendering rather than showing a blank page.
            </p>
          </div>

          {this.state.error && (
            <div className="text-left bg-gray-50 border border-gray-200 rounded-lg p-3 text-xs font-mono text-gray-700 max-w-xl mx-auto">
              <span className="font-bold text-red-700 block mb-1">Error:</span>
              <p className="break-words">{this.state.error.message}</p>
            </div>
          )}

          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <button
              type="button"
              onClick={this.handleReset}
              className="px-5 py-2.5 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg transition-all shadow-sm flex items-center gap-2 cursor-pointer"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Retry Interface</span>
            </button>

            <button
              type="button"
              onClick={() => {
                this.handleReset();
                window.location.hash = '';
                window.location.reload();
              }}
              className="px-5 py-2.5 bg-[#131921] hover:bg-slate-800 text-white font-bold text-xs rounded-lg transition-all shadow-sm flex items-center gap-2 cursor-pointer"
            >
              <Home className="w-4 h-4" />
              <span>Reload AVA Dashboard</span>
            </button>
          </div>

          {this.state.errorInfo && (
            <div className="pt-4 border-t border-gray-100 text-left max-w-xl mx-auto">
              <button
                type="button"
                onClick={() => this.setState((s) => ({ showDetails: !s.showDetails }))}
                className="text-xs text-gray-500 hover:text-gray-800 font-medium flex items-center gap-1 cursor-pointer"
              >
                <span>{this.state.showDetails ? 'Hide' : 'Show'} Component Diagnostics</span>
                {this.state.showDetails ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>

              {this.state.showDetails && (
                <pre className="mt-2 p-3 bg-gray-900 text-gray-200 rounded text-[11px] font-mono overflow-x-auto max-h-48 whitespace-pre-wrap">
                  {this.state.errorInfo.componentStack}
                </pre>
              )}
            </div>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}
