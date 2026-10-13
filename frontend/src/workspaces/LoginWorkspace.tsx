import { useState, useId } from 'react';
import type { UserProfile } from '../types';
import {
  ShieldCheck,
  User,
  Mail,
  Phone,
  MapPin,
  CheckCircle2,
  ArrowRight,
  RotateCcw,
  Sparkles,
  Lock,
} from 'lucide-react';

interface LoginWorkspaceProps {
  currentUser: UserProfile | null;
  onLoginSuccess: (profile: UserProfile) => void;
  onCancel?: () => void;
}

export function LoginWorkspace({
  currentUser,
  onLoginSuccess,
  onCancel,
}: LoginWorkspaceProps) {
  // Step 1 = Details, Step 2 = OTP, Step 3 = Success
  const [step, setStep] = useState<1 | 2 | 3>(1);

  // Form State
  const [name, setName] = useState(currentUser?.name || '');
  const [age, setAge] = useState<string>(currentUser?.age ? String(currentUser.age) : '29');
  const [gender, setGender] = useState(currentUser?.gender || 'Female');
  const [email, setEmail] = useState(currentUser?.email || '');
  const [phone, setPhone] = useState(currentUser?.phone || '');
  const [businessName, setBusinessName] = useState(currentUser?.businessName || '');
  const [address, setAddress] = useState(currentUser?.address || '');
  const [city, setCity] = useState(currentUser?.city || 'Bhubaneswar');
  const [stateName, setStateName] = useState(currentUser?.state || 'Odisha');
  const [pincode, setPincode] = useState(currentUser?.pincode || '751007');
  const [sellerCategory, setSellerCategory] = useState(
    currentUser?.sellerCategory || "Women's Kurtas & Kurtis"
  );

  // OTP State
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [otpError, setOtpError] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [resendTimer, setResendTimer] = useState(45);

  const otpInputPrefix = useId();

  // Quick fill helper
  const handleQuickFill = () => {
    setName('Vandana Mohanty');
    setAge('31');
    setGender('Female');
    setEmail('vandana.kurtis@gmail.com');
    setPhone('9861023456');
    setBusinessName('Vandana Kurtis & Handlooms');
    setAddress('Plot 142, Saheed Nagar, Industrial Estate');
    setCity('Bhubaneswar');
    setStateName('Odisha');
    setPincode('751007');
    setSellerCategory("Women's Kurtas & Kurtis");
  };

  const handleProceedToOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !email.trim() || !phone.trim()) {
      alert('Please fill in your Name, Email, and Phone number to proceed.');
      return;
    }
    setStep(2);
    setResendTimer(45);
  };

  const handleOtpChange = (index: number, value: string) => {
    if (value.length > 1) {
      // Handle paste
      const pasted = value.slice(0, 6).split('');
      const newOtp = [...otp];
      pasted.forEach((char, i) => {
        if (i < 6) newOtp[i] = char;
      });
      setOtp(newOtp);
      return;
    }

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Auto-advance
    if (value && index < 5) {
      const nextInput = document.getElementById(`${otpInputPrefix}-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleVerifyOtp = () => {
    const enteredOtp = otp.join('');
    // Requirements: "for now it should verify any code we give and show the interface"
    if (enteredOtp.length === 0) {
      setOtpError('Please enter the verification code');
      return;
    }

    setIsVerifying(true);
    setOtpError('');

    setTimeout(() => {
      setIsVerifying(false);
      const profile: UserProfile = {
        name,
        age,
        gender,
        email,
        phone,
        businessName: businessName || `${name.split(' ')[0]}'s Kurtas`,
        address,
        city,
        state: stateName,
        pincode,
        sellerCategory,
        isVerified: true,
        registeredAt: new Date().toISOString(),
      };

      setStep(3);
      onLoginSuccess(profile);
    }, 400);
  };

  return (
    <div className="max-w-3xl mx-auto py-6 px-4">
      {/* Header Badge */}
      <div className="text-center mb-8 space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-100 text-[#8a5100] text-xs font-bold border border-amber-300">
          <Sparkles className="w-3.5 h-3.5 text-[#ff9900]" />
          <span>Amazon Vendor Identity &amp; Onboarding</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-[#131b2e] tracking-tight">
          {step === 1 && 'Vendor Registration & Account Setup'}
          {step === 2 && 'Two-Factor OTP Verification'}
          {step === 3 && 'Account Verified & Ready'}
        </h1>
        <p className="text-xs sm:text-sm text-gray-500 max-w-lg mx-auto">
          {step === 1 &&
            'Register your Indian apparel manufacturing or selling unit to unlock verified marketplace diagnostics.'}
          {step === 2 &&
            `Enter the 6-digit OTP code sent to your registered Gmail (${email || 'your email'}) and Phone.`}
          {step === 3 &&
            'Your identity has been verified. You now have full access to Amazon Vendor Assist intelligence.'}
        </p>

        {/* Step Indicator */}
        <div className="flex items-center justify-center gap-3 pt-3">
          <div className="flex items-center gap-1.5 text-xs font-bold">
            <span
              className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                step >= 1 ? 'bg-[#ff9900] text-[#131921]' : 'bg-gray-200 text-gray-600'
              }`}
            >
              1
            </span>
            <span className={step === 1 ? 'text-[#131b2e]' : 'text-gray-400'}>Vendor Details</span>
          </div>
          <div className="w-8 h-0.5 bg-gray-300" />
          <div className="flex items-center gap-1.5 text-xs font-bold">
            <span
              className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                step >= 2 ? 'bg-[#ff9900] text-[#131921]' : 'bg-gray-200 text-gray-600'
              }`}
            >
              2
            </span>
            <span className={step === 2 ? 'text-[#131b2e]' : 'text-gray-400'}>OTP Verify</span>
          </div>
          <div className="w-8 h-0.5 bg-gray-300" />
          <div className="flex items-center gap-1.5 text-xs font-bold">
            <span
              className={`w-6 h-6 rounded-full flex items-center justify-center text-xs ${
                step === 3 ? 'bg-emerald-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}
            >
              ✓
            </span>
            <span className={step === 3 ? 'text-emerald-700' : 'text-gray-400'}>Completed</span>
          </div>
        </div>
      </div>

      {/* STEP 1: REGISTRATION FORM */}
      {step === 1 && (
        <form
          onSubmit={handleProceedToOtp}
          className="bg-[#ffffff] rounded-xl border border-[#e2e8f0] p-6 shadow-sm space-y-6"
        >
          {/* Quick-Fill Helper Bar */}
          <div className="flex items-center justify-between pb-4 border-b border-gray-100">
            <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">
              Step 1: Basic &amp; Business Information
            </span>
            <button
              type="button"
              onClick={handleQuickFill}
              className="text-xs font-bold text-[#007185] hover:text-[#004e5b] flex items-center gap-1 cursor-pointer bg-blue-50 hover:bg-blue-100 px-2.5 py-1 rounded transition"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Quick-Fill Sample Seller</span>
            </button>
          </div>

          {/* Personal Details Section */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-xs font-bold text-gray-700">
              <User className="w-4 h-4 text-[#ff9900]" />
              <span>1. Personal &amp; Demographic Information</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="sm:col-span-2 space-y-1">
                <label className="text-xs font-semibold text-gray-700">
                  Full Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Vandana Mohanty"
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Age</label>
                <input
                  type="number"
                  min="18"
                  max="100"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  placeholder="e.g. 29"
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Gender</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 bg-white focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                >
                  <option value="Female">Female</option>
                  <option value="Male">Male</option>
                  <option value="Non-binary">Non-binary</option>
                  <option value="Prefer not to say">Prefer not to say</option>
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">
                  Store / Brand Name
                </label>
                <input
                  type="text"
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  placeholder="e.g. Vandana Kurtis & Handlooms"
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                />
              </div>
            </div>
          </div>

          {/* Contact Details Section */}
          <div className="space-y-4 pt-2 border-t border-gray-100">
            <div className="flex items-center gap-2 text-xs font-bold text-gray-700">
              <Mail className="w-4 h-4 text-[#ff9900]" />
              <span>2. Contact &amp; Authentication Channels</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">
                  Gmail / Work Email <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="e.g. vendor@gmail.com"
                    className="w-full text-xs p-2.5 pl-8 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                  />
                  <Mail className="w-4 h-4 text-gray-400 absolute left-2.5 top-2.5 pointer-events-none" />
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">
                  Mobile Phone Number (+91) <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="tel"
                    required
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="e.g. 9861023456"
                    className="w-full text-xs p-2.5 pl-8 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                  />
                  <Phone className="w-4 h-4 text-gray-400 absolute left-2.5 top-2.5 pointer-events-none" />
                </div>
              </div>
            </div>
          </div>

          {/* Address & Cluster Section */}
          <div className="space-y-4 pt-2 border-t border-gray-100">
            <div className="flex items-center gap-2 text-xs font-bold text-gray-700">
              <MapPin className="w-4 h-4 text-[#ff9900]" />
              <span>3. Manufacturing Hub &amp; Cluster Address</span>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-gray-700">
                Street Address / Unit No.
              </label>
              <input
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="e.g. Plot 142, Saheed Nagar, Industrial Estate"
                className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">City</label>
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="e.g. Bhubaneswar"
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">State</label>
                <input
                  type="text"
                  value={stateName}
                  onChange={(e) => setStateName(e.target.value)}
                  placeholder="e.g. Odisha"
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">PIN Code</label>
                <input
                  type="text"
                  value={pincode}
                  onChange={(e) => setPincode(e.target.value)}
                  placeholder="e.g. 751007"
                  className="w-full text-xs p-2.5 rounded-lg border border-gray-300 focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-semibold text-gray-700">
                Primary Product Focus
              </label>
              <select
                value={sellerCategory}
                onChange={(e) => setSellerCategory(e.target.value)}
                className="w-full text-xs p-2.5 rounded-lg border border-gray-300 bg-white focus:outline-none focus:border-[#ff9900] focus:ring-1 focus:ring-[#ff9900]"
              >
                <option value="Women's Kurtas & Kurtis">
                  Women's Kurtas &amp; Kurtis (Active Pilot)
                </option>
                <option value="Sarees">Sarees &amp; Handloom Drapes</option>
                <option value="Men's Ethnic Wear">Men's Kurtas &amp; Nehru Jackets</option>
                <option value="Western Tops & Tunics">Western Tops &amp; Casual Shirts</option>
              </select>
            </div>
          </div>

          {/* Action Footer */}
          <div className="pt-4 border-t border-gray-200 flex items-center justify-between">
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="text-xs font-semibold text-gray-500 hover:text-gray-800"
              >
                Cancel
              </button>
            )}
            <button
              type="submit"
              className="ml-auto px-6 py-2.5 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg transition-all shadow-md flex items-center gap-2 cursor-pointer active:scale-95"
            >
              <span>Proceed to OTP Verification</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      )}

      {/* STEP 2: OTP VERIFICATION SCREEN */}
      {step === 2 && (
        <div className="bg-[#ffffff] rounded-xl border border-[#e2e8f0] p-6 sm:p-8 shadow-sm space-y-6 max-w-lg mx-auto">
          <div className="text-center space-y-2">
            <div className="w-12 h-12 rounded-full bg-amber-50 text-[#8a5100] flex items-center justify-center mx-auto border border-amber-200">
              <Lock className="w-6 h-6 text-[#ff9900]" />
            </div>
            <h2 className="text-lg font-bold text-gray-900">Enter Verification Code</h2>
            <p className="text-xs text-gray-500">
              We have dispatched a 6-digit one-time code to:
            </p>
            <div className="inline-block bg-slate-50 border border-slate-200 rounded px-3 py-1 font-mono text-xs text-gray-700">
              +91 {phone} · {email}
            </div>
          </div>

          {/* Demo Sandbox Alert */}
          <div className="p-3 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <div className="leading-relaxed">
              <strong className="font-bold">Sandbox Verification Mode:</strong> Enter any 4 to
              6 digits (e.g. <span className="font-mono font-bold">123456</span>) to verify
              instantly and launch the AVA platform.
            </div>
          </div>

          {/* 6 Digit Input Boxes */}
          <div className="space-y-2">
            <div className="flex items-center justify-center gap-2 sm:gap-3">
              {otp.map((digit, idx) => (
                <input
                  key={idx}
                  id={`${otpInputPrefix}-${idx}`}
                  type="text"
                  maxLength={1}
                  value={digit}
                  onChange={(e) => handleOtpChange(idx, e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Backspace' && !otp[idx] && idx > 0) {
                      const prevInput = document.getElementById(`${otpInputPrefix}-${idx - 1}`);
                      prevInput?.focus();
                    }
                  }}
                  className="w-11 h-12 text-center text-lg font-mono font-bold rounded-lg border-2 border-gray-300 focus:border-[#ff9900] focus:ring-2 focus:ring-[#ff9900]/20 focus:outline-none"
                />
              ))}
            </div>
            {otpError && (
              <p className="text-center text-xs text-red-600 font-semibold">{otpError}</p>
            )}
          </div>

          {/* Resend Timer */}
          <div className="text-center text-xs text-gray-500">
            {resendTimer > 0 ? (
              <span>Resend OTP in {resendTimer}s</span>
            ) : (
              <button
                type="button"
                onClick={() => setResendTimer(45)}
                className="font-bold text-[#007185] hover:underline cursor-pointer"
              >
                Resend Verification Code
              </button>
            )}
          </div>

          {/* Verification Actions */}
          <div className="space-y-2 pt-2">
            <button
              type="button"
              disabled={isVerifying}
              onClick={handleVerifyOtp}
              className="w-full py-3 bg-[#ff9900] hover:bg-[#f08800] text-[#131921] font-bold text-xs rounded-lg transition-all shadow-md flex items-center justify-center gap-2 cursor-pointer active:scale-95 disabled:opacity-50"
            >
              {isVerifying ? (
                <>
                  <RotateCcw className="w-4 h-4 animate-spin" />
                  <span>Verifying Credentials...</span>
                </>
              ) : (
                <>
                  <ShieldCheck className="w-4 h-4" />
                  <span>Verify Code &amp; Access AVA</span>
                </>
              )}
            </button>

            <button
              type="button"
              onClick={() => setStep(1)}
              className="w-full py-2 text-xs font-semibold text-gray-500 hover:text-gray-800 transition"
            >
              ← Edit Registration Details
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: SUCCESS STATE */}
      {step === 3 && (
        <div className="bg-[#ffffff] rounded-xl border border-emerald-200 p-8 shadow-sm space-y-6 text-center max-w-md mx-auto">
          <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center mx-auto border-2 border-emerald-300">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h2 className="text-xl font-black text-gray-900">Identity Verified!</h2>
            <p className="text-xs text-gray-600">
              Welcome, <strong className="text-gray-900">{name}</strong>. Your Seller Central profile for{' '}
              <strong className="text-gray-900">{businessName}</strong> is now authenticated on the AVA platform.
            </p>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-left space-y-1.5 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-500">Registered Vendor:</span>
              <span className="font-bold text-gray-900">{name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Business Unit:</span>
              <span className="font-bold text-gray-900">{businessName}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Cluster Location:</span>
              <span className="font-bold text-gray-900">{city}, {stateName}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-500">Product Focus:</span>
              <span className="font-bold text-amber-700">{sellerCategory}</span>
            </div>
          </div>

          <button
            type="button"
            onClick={() => {
              if (onCancel) onCancel();
            }}
            className="w-full py-3 bg-[#131921] hover:bg-slate-800 text-white font-bold text-xs rounded-lg transition flex items-center justify-center gap-2 cursor-pointer shadow"
          >
            <span>Proceed to AVA Platform</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
